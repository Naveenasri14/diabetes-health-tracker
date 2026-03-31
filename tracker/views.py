from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Q

from datetime import datetime, date, timedelta
import json
import re

from .models import (
    GlucoseRecord, BPRecord, NotificationPreference,
    Reminder, NotificationLog, UserProfile, CaregiverLink
)
from django.contrib.auth.models import User


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
        form = UserCreationForm(request.POST)
        role   = request.POST.get('role', '').strip()
        region = request.POST.get('region', '').strip()
        email  = request.POST.get('email', '').strip()
        phone  = request.POST.get('phone', '').strip()

        # Validate custom fields
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

        form_valid = form.is_valid()

        # Collect unique form errors
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

        # Save user & profile
        user = form.save()
        profile_obj = UserProfile.objects.create(
            user=user,
            role=role,
            region=region.lower().strip(),
            email=email,
            phone=phone,
        )

        # FIX 4: If registering as caregiver, auto-accept any pending links
        # where a patient added this phone/email before the caregiver had an account
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
                messages.info(
                    request,
                    f"You have been linked to {count} patient(s) who already added you!"
                )

        # FIX 3: Single success message only
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
            return redirect('/dashboard/')
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
    print("🔥 redirect_dashboard called")
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        print("❌ No profile found")
        messages.error(request, "Profile not found.")
        return redirect('login_view')
    
    print("👉 ROLE:", profile.role)

    # ── PATIENT ──
    if profile.role == 'patient':
        is_first_login = (
            not CaregiverLink.objects.filter(patient=profile).exists() and
            not GlucoseRecord.objects.filter(user=request.user).exists()
        )
        
        print("👉 is_first_login:", is_first_login)

        if is_first_login and not profile.has_skipped_caregiver:
            return redirect('add_caregiver')

        # ✅ FIX: send to patient dashboard (NOT generic dashboard)
        print("➡ Redirecting to patient_dashboard")
        return redirect('patient_dashboard')

    # ── CAREGIVER ──
    elif profile.role == 'caregiver':
        print("➡ Redirecting to caregiver_dashboard")
        return redirect('caregiver_dashboard')

    # fallback
    return redirect('patient_dashboard')

# ──────────────────────────────────────────
# DASHBOARDS
# ──────────────────────────────────────────

@login_required
def dashboard(request):
    glucose_records = GlucoseRecord.objects.filter(user=request.user).order_by('-date')
    bp_records = BPRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, "dashboard.html", {
        'glucose_records': glucose_records,
        'bp_records': bp_records,
    })


@login_required
def patient_dashboard(request):
    profile = request.user.userprofile
    recent_glucose = GlucoseRecord.objects.filter(
        user=request.user).order_by('-date', '-time')[:5]
    my_caregivers = CaregiverLink.objects.filter(patient=profile)
    # FIX 5: health workers in same region shown to patient

    return render(request, 'patient_dashboard.html', {
        'profile':        profile,
        'recent_glucose': recent_glucose,
        'my_caregivers':  my_caregivers,
    })


@login_required
def caregiver_dashboard(request):
    """FIX 4: Caregiver sees all linked patients and their latest records."""
    profile = request.user.userprofile

    accepted_links = CaregiverLink.objects.filter(
        caregiver_profile=profile,
        status='accepted'
    ).select_related('patient__user')

    patients_data = []
    for link in accepted_links:
        p = link.patient
        recent_glucose = GlucoseRecord.objects.filter(
            user=p.user).order_by('-date', '-time')[:3]
        recent_bp = BPRecord.objects.filter(
            user=p.user).order_by('-date')[:2]
        latest = recent_glucose.first()
        risk = 'high'   if latest and latest.glucose_level > 250 else \
               'low'    if latest and latest.glucose_level < 70  else \
               'normal' if latest else 'no_data'

        patients_data.append({
            'link':           link,
            'profile':        p,
            'recent_glucose': recent_glucose,
            'recent_bp':      recent_bp,
            'risk':           risk,
            'latest_reading': latest,
        })

    alerts = [p for p in patients_data if p['risk'] in ['high', 'low']]
    return render(request, 'caregiver_dashboard.html', {
        'profile':       profile,
        'patients_data': patients_data,
        'alerts': alerts,
    })


# ──────────────────────────────────────────
# CAREGIVER SETUP
# ──────────────────────────────────────────

@login_required
def add_caregiver(request):
    # 🔥 Auto-skip for non-patient roles
    if request.user.userprofile.role != 'patient':
        return redirect('redirect_dashboard')
    profile = request.user.userprofile
    if profile.role != 'patient':
        return redirect('redirect_dashboard')

    existing_links = CaregiverLink.objects.filter(patient=profile)

    if request.method == 'POST':
        action = request.POST.get('action')
        print("👉 ACTION:", action)

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

            added = 0
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
                    row_errors.append(
                        f"'{phone}' is not a valid 10-digit Indian mobile number.")
                if not email or not is_valid_email(email):
                    row_errors.append(
                        f"'{email}' is not a valid email address.")

                if row_errors:
                    errors.extend(row_errors)
                    continue

                if CaregiverLink.objects.filter(
                        patient=profile, caregiver_phone=phone).exists():
                    errors.append(f"Caregiver with number {phone} already added.")
                    continue

                # Auto-link if caregiver already has account
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
                messages.success(
                    request,
                    f"{added} caregiver(s) added successfully!"
                )
            if errors:
                return redirect('add_caregiver')
            return redirect('patient_dashboard')

    return render(request, 'caregiver.html', {
        'profile':        profile,
        'existing_links': existing_links,
    })


# ──────────────────────────────────────────
# PROFILE
# ──────────────────────────────────────────

@login_required
def profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        new_phone  = request.POST.get('phone', '').strip()
        new_email  = request.POST.get('email', '').strip()
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
    return render(request, 'profile.html', {'profile': user_profile})


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
        'today_date':    date.today().isoformat(),
        'current_time':  datetime.now().strftime('%H:%M'),
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
    return render(request, "add_bp.html", {
        'today_date': date.today().isoformat()})


@login_required
def bp_page(request):
    records = BPRecord.objects.filter(user=request.user).order_by('-date')
    total   = records.count()
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
        Reminder.objects.create(
            user=request.user,
            reminder_type=request.POST.get('reminder_type'),
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            frequency=request.POST.get('frequency'),
            reminder_time=request.POST.get('reminder_time'),
            start_date=request.POST.get('start_date') or date.today(),
            is_active=True,
        )
        messages.success(request, 'Reminder created!')
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
    now = datetime.now()
    active = Reminder.objects.filter(
        user=request.user, is_active=True,
        start_date__lte=now.date(),
        reminder_time__lte=now.time(),
    ).first()
    if active:
        return JsonResponse({
            'has_alarm': True,
            'reminder_id': active.id,
            'title': active.title,
        })
    return JsonResponse({'has_alarm': False})


# ──────────────────────────────────────────
# AI PREDICTION
# ──────────────────────────────────────────

@login_required
def ai_prediction(request):
    return render(request, "ai_prediction.html")


# ──────────────────────────────────────────
# HEALTH WORKER ADMIN DASHBOARD
# ──────────────────────────────────────────

@login_required
def admin_dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('dashboard')

    if profile.role not in ['caregiver']:
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


@login_required
def manage_links(request):
    return render(request, 'add_caregiver.html')