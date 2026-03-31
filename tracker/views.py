from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, date, timedelta
import json
import re

from .models import (
    GlucoseRecord, BPRecord, NotificationPreference,
    Reminder, NotificationLog, UserProfile, CaregiverLink,
    CaregiverNote, CaregiverMessage, PatientAlert,
)
from .services.ai_chatbot import get_bot_response


# ──────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────

def is_valid_indian_phone(phone):
    return bool(re.match(r'^[6-9]\d{9}$', phone.strip()))

def is_valid_email(email):
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email.strip()))


# ──────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────

def signup(request):
    if request.method == 'POST':
        form   = UserCreationForm(request.POST)
        role   = request.POST.get('role', '').strip()
        region = request.POST.get('region', '').strip()
        email  = request.POST.get('email', '').strip()
        phone  = request.POST.get('phone', '').strip()

        custom_errors = []
        if not role:
            custom_errors.append("Please select a role.")
        if not region:
            custom_errors.append("Region / village is required.")
        if not email:
            custom_errors.append("Email is required.")
        elif not is_valid_email(email):
            custom_errors.append("Enter a valid email address (e.g. name@gmail.com).")
        if not phone:
            custom_errors.append("Mobile number is required.")
        elif not is_valid_indian_phone(phone):
            custom_errors.append("Enter a valid 10-digit Indian mobile number starting with 6-9.")

        form_valid  = form.is_valid()
        form_errors = []
        if not form_valid:
            seen = set()
            for field, errs in form.errors.items():
                for e in errs:
                    clean = re.sub(r'<[^>]+>', '', str(e)).strip()
                    if clean not in seen:
                        seen.add(clean)
                        form_errors.append(clean)

        all_errors = form_errors + custom_errors
        if all_errors:
            for e in all_errors:
                messages.error(request, e)
            return render(request, 'signup.html', {'form': form})

        user = form.save()
        profile_obj = UserProfile.objects.create(
            user=user,
            role=role,
            region=region.lower().strip(),
            email=email,
            phone=phone,
        )

        # Auto-link caregiver: accept any pending links that already reference this phone/email
        if role == 'caregiver':
            pending = CaregiverLink.objects.filter(
                caregiver_profile__isnull=True,
                status='pending'
            ).filter(Q(caregiver_phone=phone) | Q(caregiver_email=email))
            count = pending.count()
            for link in pending:
                link.caregiver_profile = profile_obj
                link.status = 'accepted'
                link.save()
            if count:
                messages.info(request,
                    f"You have been linked to {count} patient(s) who already added you!")

        messages.success(request, "Account created! Please log in.")
        return redirect('login_view')

    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('redirect_dashboard')
        messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


# ──────────────────────────────────────────
# ROLE-BASED REDIRECT
# ──────────────────────────────────────────

@login_required
def redirect_dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login_view')

    if profile.role == 'patient':
        is_first_login = (
            not CaregiverLink.objects.filter(patient=profile).exists() and
            not GlucoseRecord.objects.filter(user=request.user).exists()
        )
        if is_first_login and not profile.has_skipped_caregiver:
            return redirect('add_caregiver')
        return redirect('patient_dashboard')

    elif profile.role == 'caregiver':
        return redirect('caregiver_dashboard')

    elif profile.role == 'health_worker':
        return redirect('health_worker_dashboard')

    return redirect('dashboard')


# ──────────────────────────────────────────
# DASHBOARDS
# ──────────────────────────────────────────

@login_required
def dashboard(request):
    glucose_records = GlucoseRecord.objects.filter(user=request.user).order_by('-date')
    bp_records      = BPRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, "dashboard.html", {
        'glucose_records': glucose_records,
        'bp_records':      bp_records,
    })


@login_required
def patient_dashboard(request):
    profile        = request.user.userprofile
    recent_glucose = GlucoseRecord.objects.filter(
        user=request.user).order_by('-date', '-time')[:5]
    my_caregivers  = CaregiverLink.objects.filter(patient=profile)

    # Health workers in same region
    region_workers = UserProfile.objects.filter(
        role='health_worker',
        region__iexact=profile.region
    ).select_related('user')

    # Unread messages from caregivers
    unread_messages = CaregiverMessage.objects.filter(
        patient=profile, is_read=False).order_by('-sent_at')

    return render(request, 'patient_dashboard.html', {
        'profile':          profile,
        'recent_glucose':   recent_glucose,
        'my_caregivers':    my_caregivers,
        'region_workers':   region_workers,
        'unread_messages':  unread_messages,
    })


@login_required
def caregiver_dashboard(request):
    """
    Full caregiver dashboard:
    - Smart alerts (high/low/emergency glucose, inactivity)
    - Per-patient notes, unread message counts
    - Color-coded risk cards
    - Region/location-based patient grouping context
    """
    from django.utils import timezone as tz
    profile = request.user.userprofile
    today   = tz.now().date()

    accepted_links = CaregiverLink.objects.filter(
        caregiver_profile=profile,
        status='accepted'
    ).select_related('patient__user')

    patients_data = []
    alerts        = []

    for link in accepted_links:
        p              = link.patient
        recent_glucose = GlucoseRecord.objects.filter(
            user=p.user).order_by('-date', '-time')[:5]
        recent_bp      = BPRecord.objects.filter(
            user=p.user).order_by('-date')[:2]
        latest         = recent_glucose.first()

        # Risk level (feature #1 / #5 – smart alerts + emergency flag)
        if latest:
            g = latest.glucose_level
            if g > 300:    risk = 'emergency'
            elif g > 250:  risk = 'high'
            elif g < 70:   risk = 'low'
            elif g <= 140: risk = 'normal'
            else:          risk = 'prediabetes'
        else:
            risk = 'no_data'

        # Inactivity detection (feature #1)
        inactive      = False
        inactive_days = 0
        hours_since   = None
        if latest:
            inactive_days = (today - latest.date).days
            inactive      = inactive_days >= 2
            # "Last updated X hours ago"
            last_dt     = datetime.combine(latest.date, latest.time)
            hours_since = int((datetime.now() - last_dt).total_seconds() // 3600)

        readings_today = GlucoseRecord.objects.filter(
            user=p.user, date=today).count()

        # Notes by this caregiver for this patient (feature #8)
        notes = CaregiverNote.objects.filter(
            caregiver=profile, patient=p).order_by('-created_at')

        # Unread messages count (feature #2)
        unread_msgs = CaregiverMessage.objects.filter(
            caregiver=profile, patient=p, is_read=False).count()

        # Last BP for health summary (feature #10)
        last_bp = recent_bp.first()

        entry = {
            'link':           link,
            'profile':        p,
            'recent_glucose': recent_glucose,
            'recent_bp':      recent_bp,
            'last_bp':        last_bp,
            'risk':           risk,
            'latest_reading': latest,
            'hours_since':    hours_since,
            'inactive':       inactive,
            'inactive_days':  inactive_days,
            'readings_today': readings_today,
            'notes':          notes,
            'unread_msgs':    unread_msgs,
        }
        patients_data.append(entry)
        if risk in ('high', 'low', 'emergency') or inactive:
            alerts.append(entry)

    high_risk_count = sum(1 for p in patients_data if p['risk'] in ('high', 'emergency'))
    inactive_count  = sum(1 for p in patients_data if p['inactive'])

    return render(request, 'caregiver_dashboard.html', {
        'profile':          profile,
        'patients_data':    patients_data,
        'alerts':           alerts,
        'high_risk_count':  high_risk_count,
        'inactive_count':   inactive_count,
        'message_types':    CaregiverMessage.MESSAGE_TYPES,
    })


@login_required
def health_worker_dashboard(request):
    """Health worker sees all patients in same region (feature #6)."""
    profile = request.user.userprofile

    patients = UserProfile.objects.filter(
        role='patient',
        region__iexact=profile.region
    ).select_related('user')

    patient_summaries = []
    for p in patients:
        latest = GlucoseRecord.objects.filter(
            user=p.user).order_by('-date', '-time').first()
        risk = 'high'   if latest and latest.glucose_level > 250 else \
               'low'    if latest and latest.glucose_level < 70  else \
               'normal' if latest else 'no_data'
        missed     = GlucoseRecord.objects.filter(user=p.user, medication_taken=False).count()
        caregivers = CaregiverLink.objects.filter(patient=p, status='accepted').count()

        patient_summaries.append({
            'profile':         p,
            'latest_reading':  latest,
            'risk':            risk,
            'missed_meds':     missed,
            'caregiver_count': caregivers,
        })

    return render(request, 'health_worker_dashboard.html', {
        'profile':           profile,
        'patient_summaries': patient_summaries,
        'total_patients':    patients.count(),
        'high_risk_count':   sum(1 for p in patient_summaries if p['risk'] == 'high'),
        'missed_med_count':  sum(1 for p in patient_summaries if p['missed_meds'] > 0),
    })


# ──────────────────────────────────────────
# CAREGIVER SETUP
# ──────────────────────────────────────────

@login_required
def add_caregiver(request):
    profile = request.user.userprofile
    if profile.role != 'patient':
        return redirect('redirect_dashboard')

    existing_links = CaregiverLink.objects.filter(patient=profile)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'skip':
            profile.has_skipped_caregiver = True
            profile.save()
            return redirect('patient_dashboard')

        if action == 'remove':
            link_id = request.POST.get('link_id')
            get_object_or_404(CaregiverLink, id=link_id, patient=profile).delete()
            messages.success(request, 'Caregiver removed.')
            return redirect('add_caregiver')

        if action == 'add_caregivers':
            names  = request.POST.getlist('caregiver_name[]')
            phones = request.POST.getlist('caregiver_phone[]')
            emails = request.POST.getlist('caregiver_email[]')

            added  = 0
            errors = []

            for name, phone, email in zip(names, phones, emails):
                name  = name.strip()
                phone = phone.strip()
                email = email.strip()

                if not name and not phone and not email:
                    continue

                row_errors = []
                if not name:
                    row_errors.append("Caregiver name is required.")
                if not phone or not is_valid_indian_phone(phone):
                    row_errors.append(f"'{phone}' is not a valid 10-digit Indian mobile number.")
                if not email or not is_valid_email(email):
                    row_errors.append(f"'{email}' is not a valid email address.")

                if row_errors:
                    errors.extend(row_errors)
                    continue

                if CaregiverLink.objects.filter(patient=profile, caregiver_phone=phone).exists():
                    errors.append(f"Caregiver with number {phone} already added.")
                    continue

                existing_cg = UserProfile.objects.filter(
                    role='caregiver'
                ).filter(Q(phone=phone) | Q(email=email)).first()

                CaregiverLink.objects.create(
                    patient=profile,
                    caregiver_name=name,
                    caregiver_phone=phone,
                    caregiver_email=email,
                    caregiver_profile=existing_cg,
                    status='accepted' if existing_cg else 'pending',
                )
                added += 1

            for e in errors:
                messages.error(request, e)
            if added:
                messages.success(request, f"{added} caregiver(s) added successfully!")
            if errors:
                return redirect('add_caregiver')
            return redirect('patient_dashboard')

    return render(request, 'add_caregiver.html', {
        'profile':        profile,
        'existing_links': existing_links,
    })


@login_required
def manage_links(request):
    return render(request, 'add_caregiver.html')


# ──────────────────────────────────────────
# CAREGIVER ACTIONS  (feature #2, #8, #9)
# ──────────────────────────────────────────

@login_required
def caregiver_add_note(request, patient_username):
    """Caregiver adds or edits a note for a patient (feature #8)."""
    caregiver_profile = request.user.userprofile
    patient_user      = get_object_or_404(User, username=patient_username)
    patient_profile   = patient_user.userprofile

    if not CaregiverLink.objects.filter(
        caregiver_profile=caregiver_profile,
        patient=patient_profile, status='accepted'
    ).exists():
        messages.error(request, "You are not linked to this patient.")
        return redirect('caregiver_dashboard')

    if request.method == 'POST':
        note_text = request.POST.get('note', '').strip()
        note_id   = request.POST.get('note_id', '')
        if not note_text:
            messages.error(request, "Note cannot be empty.")
            return redirect('caregiver_dashboard')
        if note_id:
            note = get_object_or_404(CaregiverNote, id=note_id, caregiver=caregiver_profile)
            note.note = note_text
            note.save()
            messages.success(request, "Note updated.")
        else:
            CaregiverNote.objects.create(
                caregiver=caregiver_profile,
                patient=patient_profile,
                note=note_text,
            )
            messages.success(request, "Note saved.")
    return redirect('caregiver_dashboard')


@login_required
def caregiver_delete_note(request, note_id):
    note = get_object_or_404(CaregiverNote, id=note_id, caregiver=request.user.userprofile)
    note.delete()
    messages.success(request, "Note deleted.")
    return redirect('caregiver_dashboard')


@login_required
def caregiver_send_message(request, patient_username):
    """Caregiver sends a quick alert message to a patient (feature #2)."""
    caregiver_profile = request.user.userprofile
    patient_user      = get_object_or_404(User, username=patient_username)
    patient_profile   = patient_user.userprofile

    if not CaregiverLink.objects.filter(
        caregiver_profile=caregiver_profile,
        patient=patient_profile, status='accepted'
    ).exists():
        messages.error(request, "You are not linked to this patient.")
        return redirect('caregiver_dashboard')

    if request.method == 'POST':
        msg_type    = request.POST.get('message_type', 'check_glucose')
        custom_text = request.POST.get('custom_text', '').strip()
        CaregiverMessage.objects.create(
            caregiver=caregiver_profile,
            patient=patient_profile,
            message_type=msg_type,
            custom_text=custom_text if msg_type == 'custom' else '',
        )
        label = dict(CaregiverMessage.MESSAGE_TYPES).get(msg_type, msg_type)
        NotificationLog.objects.create(
            user=patient_user,
            notification_type='in_app',
            title=f"Message from your caregiver {request.user.username}",
            message=custom_text if msg_type == 'custom' else label,
            status='sent',
        )
        messages.success(request, f"Message sent to {patient_username}.")
    return redirect('caregiver_dashboard')


@login_required
def patient_messages(request):
    """Patient views messages sent by caregivers."""
    profile = request.user.userprofile
    msgs    = CaregiverMessage.objects.filter(patient=profile).order_by('-sent_at')[:30]
    CaregiverMessage.objects.filter(patient=profile, is_read=False).update(is_read=True)
    return render(request, 'patient_messages.html', {
        'messages_list': msgs,
        'profile':       profile,
    })


# ──────────────────────────────────────────
# PROFILE
# ──────────────────────────────────────────

@login_required
def profile(request):
    user_profile = request.user.userprofile
    is_patient   = user_profile.role == 'patient'
    if request.method == 'POST':
        new_phone  = request.POST.get('phone',  '').strip()
        new_email  = request.POST.get('email',  '').strip()
        new_region = request.POST.get('region', '').strip()
        errs = []
        if new_phone and not is_valid_indian_phone(new_phone):
            errs.append("Invalid phone number.")
        if new_email and not is_valid_email(new_email):
            errs.append("Invalid email address.")
        if errs:
            for e in errs:
                messages.error(request, e)
        else:
            user_profile.phone  = new_phone  or user_profile.phone
            user_profile.email  = new_email  or user_profile.email
            user_profile.region = new_region.lower() or user_profile.region
            user_profile.save()
            messages.success(request, "Profile updated!")
        return redirect('profile')
    return render(request, 'profile.html', {
        'profile':    user_profile,
        'is_patient': is_patient,
    })


# ──────────────────────────────────────────
# GLUCOSE RECORDS
# ──────────────────────────────────────────

@login_required
def add_record(request):
    if request.method == 'POST':
        symptoms_str = ','.join(request.POST.getlist('symptoms'))
        GlucoseRecord.objects.create(
            user=request.user,
            glucose_level=request.POST.get('glucose_level'),
            date=request.POST.get('date') or date.today(),
            time=request.POST.get('time') or datetime.now().time(),
            reading_type=request.POST.get('reading_type'),
            meal_type=request.POST.get('meal_type') or None,
            food_notes=request.POST.get('food_notes', ''),
            medication_taken=request.POST.get('medication_taken') == 'on',
            medicine_name=request.POST.get('medicine_name', ''),
            insulin_dose=request.POST.get('insulin_dose') or None,
            activity_type=request.POST.get('activity_type') or None,
            activity_duration=request.POST.get('activity_duration') or None,
            symptoms=symptoms_str,
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Glucose record saved!')
        return redirect('glucose')

    return render(request, 'add_record.html', {
        'today_date':   date.today().isoformat(),
        'current_time': datetime.now().strftime('%H:%M'),
    })


@login_required
def glucose_page(request):
    records = GlucoseRecord.objects.filter(
        user=request.user).order_by('-date', '-time')
    total = records.count()

    if total:
        avg_glucose       = sum(r.glucose_level for r in records) / total
        estimated_a1c     = round((avg_glucose + 46.7) / 28.7, 1)
        high_count        = sum(1 for r in records if r.get_glucose_category() == 'high')
        low_count         = sum(1 for r in records if r.get_glucose_category() == 'low')
        normal_count      = sum(1 for r in records if r.get_glucose_category() == 'normal')
        prediabetes_count = sum(1 for r in records if r.get_glucose_category() == 'prediabetes')
    else:
        avg_glucose = estimated_a1c = 0
        high_count = low_count = normal_count = prediabetes_count = 0

    return render(request, 'glucose.html', {
        'glucose_records':   records,
        'avg_glucose':       round(avg_glucose, 1),
        'estimated_a1c':     estimated_a1c,
        'high_count':        high_count,
        'low_count':         low_count,
        'normal_count':      normal_count,
        'prediabetes_count': prediabetes_count,
        'total_records':     total,
    })


# ──────────────────────────────────────────
# BLOOD PRESSURE
# ──────────────────────────────────────────

@login_required
def add_bp(request):
    if request.method == "POST":
        BPRecord.objects.create(
            user=request.user,
            systolic=request.POST.get('systolic'),
            diastolic=request.POST.get('diastolic'),
            pulse=request.POST.get('pulse') or None,
            date=request.POST.get('date') or date.today(),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'BP record added!')
        return redirect('bp')
    return render(request, "add_bp.html", {'today_date': date.today().isoformat()})


@login_required
def bp_page(request):
    records      = BPRecord.objects.filter(user=request.user).order_by('-date')
    total        = records.count()
    avg_systolic = avg_diastolic = 0
    if total:
        avg_systolic  = round(sum(r.systolic  for r in records) / total, 1)
        avg_diastolic = round(sum(r.diastolic for r in records) / total, 1)
    return render(request, 'bp.html', {
        'bp_records':    records,
        'avg_systolic':  avg_systolic,
        'avg_diastolic': avg_diastolic,
        'total_records': total,
    })


# ──────────────────────────────────────────
# REMINDERS
# ──────────────────────────────────────────

@login_required
def reminder_settings(request):
    prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        prefs.email_enabled = request.POST.get('email_enabled') == 'on'
        prefs.sms_enabled   = request.POST.get('sms_enabled') == 'on'
        prefs.email_address = request.POST.get('email_address', '')
        prefs.phone_number  = request.POST.get('phone_number', '')
        prefs.carrier       = request.POST.get('carrier', '')
        prefs.save()
        messages.success(request, 'Preferences updated!')
        return redirect('reminder_settings')

    return render(request, 'reminder_settings.html', {
        'prefs':             prefs,
        'reminders':         Reminder.objects.filter(
                                 user=request.user).order_by('reminder_time'),
        'reminder_types':    Reminder.REMINDER_TYPES,
        'frequency_choices': Reminder.FREQUENCY_CHOICES,
        'today_date':        date.today().isoformat(),
    })


@login_required
def add_reminder(request):
    if request.method == 'POST':
        try:
            start_date_str = request.POST.get('start_date')
            start_date_val = (
                datetime.strptime(start_date_str, '%Y-%m-%d').date()
                if start_date_str else date.today()
            )
            frequency     = request.POST.get('frequency')
            specific_date = start_date_val if frequency == 'once' else None

            Reminder.objects.create(
                user=request.user,
                reminder_type=request.POST.get('reminder_type'),
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                frequency=frequency,
                reminder_time=request.POST.get('reminder_time'),
                start_date=start_date_val,
                specific_date=specific_date,
                days_of_week=request.POST.get('days_of_week', ''),
                medication_name=request.POST.get('medication_name', ''),
                medication_dosage=request.POST.get('medication_dosage', ''),
                is_active=True,
                notify_in_app=True,
                notify_email=request.POST.get('notify_email') == 'on',
            )
            messages.success(request, 'Reminder created!')
        except Exception as e:
            messages.error(request, f'Error creating reminder: {str(e)}')
    return redirect('reminder_settings')


@login_required
def delete_reminder(request, reminder_id):
    get_object_or_404(Reminder, id=reminder_id, user=request.user).delete()
    messages.success(request, 'Reminder deleted.')
    return redirect('reminder_settings')


@login_required
def toggle_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.is_active = not reminder.is_active
    reminder.save()
    return redirect('reminder_settings')


# ──────────────────────────────────────────
# ALARMS
# ──────────────────────────────────────────

@login_required
def show_alarm(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    NotificationLog.objects.create(
        user=request.user, reminder=reminder,
        notification_type='in_app',
        title=f'Alarm: {reminder.title}',
        message='Alarm triggered', status='sent',
    )
    return render(request, 'reminder_alarm.html', {'reminder': reminder})


@login_required
def dismiss_alarm(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    messages.success(request, f'Alarm dismissed for {reminder.title}')
    return redirect('dashboard')


@login_required
def snooze_alarm(request, reminder_id):
    reminder    = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    snooze_time = datetime.now() + timedelta(minutes=5)
    Reminder.objects.create(
        user=request.user,
        reminder_type=reminder.reminder_type,
        title=f"SNOOZED: {reminder.title}",
        description="Snoozed reminder",
        frequency='once',
        reminder_time=snooze_time.time(),
        start_date=date.today(),
        specific_date=date.today(),
        is_active=True,
    )
    reminder.is_active = False
    reminder.save()
    messages.info(request, f"Snoozed until {snooze_time.strftime('%H:%M')}")
    return redirect('dashboard')


@login_required
def check_active_alarms(request):
    now    = datetime.now()
    active = Reminder.objects.filter(
        user=request.user, is_active=True,
        start_date__lte=now.date(),
        reminder_time__lte=now.time(),
    ).first()
    if active:
        return JsonResponse({
            'has_alarm':   True,
            'reminder_id': active.id,
            'title':       active.title,
        })
    return JsonResponse({'has_alarm': False})


# ──────────────────────────────────────────
# AI PREDICTION
# ──────────────────────────────────────────

@login_required
def ai_prediction(request):
    return render(request, "ai_prediction.html")


# ──────────────────────────────────────────
# HEALTH WORKER / ADMIN DASHBOARD
# ──────────────────────────────────────────

@login_required
def admin_dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('dashboard')

    if profile.role not in ('health_worker', 'caregiver'):
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    region_patients   = UserProfile.objects.filter(
        role='patient', region__iexact=profile.region)
    total_users       = region_patients.count()
    high_risk         = GlucoseRecord.objects.filter(
        user__userprofile__in=region_patients, glucose_level__gt=250).count()
    missed_medication = GlucoseRecord.objects.filter(
        user__userprofile__in=region_patients, medication_taken=False).count()
    recent_alerts     = NotificationLog.objects.filter(
        user__userprofile__in=region_patients).order_by('-sent_at')[:10]

    return render(request, 'admin_dashboard.html', {
        'total_users':       total_users,
        'high_risk':         high_risk,
        'missed_medication': missed_medication,
        'recent_alerts':     recent_alerts,
    })


# ──────────────────────────────────────────
# EXTRA PAGES
# ──────────────────────────────────────────

def accessibility(request):
    return render(request, "accessibility.html")


def ai_assistant(request):
    return render(request, "ai_assistant.html")


@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        reply   = get_bot_response(message)
        return JsonResponse({"response": reply})
    return JsonResponse({"error": "POST required"}, status=405)