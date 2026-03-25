from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

from datetime import datetime, date, timedelta
import json

from .models import GlucoseRecord, BPRecord, NotificationPreference, Reminder, NotificationLog
from .models import UserProfile


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        role = request.POST.get('role')
        region = request.POST.get('region')

        if form.is_valid():
            user = form.save()
            
            # Save user profile with role and region
            UserProfile.objects.create(
                user=user,
                role=role,
                region=region
            )
            
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# ---------------- AUTH ---------------- #

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error_message': 'Invalid username or password!'
            })

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- PROFILE ---------------- #

@login_required
def profile(request):
    return render(request, 'profile.html')


# ---------------- DASHBOARD ---------------- #

@login_required
def dashboard(request):

    glucose_records = GlucoseRecord.objects.filter(user=request.user).order_by('-date')
    bp_records = BPRecord.objects.filter(user=request.user).order_by('-date')

    context = {
        'glucose_records': glucose_records,
        'bp_records': bp_records
    }

    return render(request, "dashboard.html", context)


# ---------------- GLUCOSE RECORD ---------------- #

@login_required
def add_record(request):

    if request.method == 'POST':

        symptoms = request.POST.getlist('symptoms')
        symptoms_str = ','.join(symptoms) if symptoms else ''

        GlucoseRecord.objects.create(
            user=request.user,
            glucose_level=request.POST.get('glucose_level'),
            date=request.POST.get('date') or date.today(),
            time=request.POST.get('time') or datetime.now().time(),
            reading_type=request.POST.get('reading_type'),
            meal_type=request.POST.get('meal_type'),
            food_notes=request.POST.get('food_notes', ''),
            medication_taken=request.POST.get('medication_taken') == 'on',
            medicine_name=request.POST.get('medicine_name', ''),
            insulin_dose=request.POST.get('insulin_dose') or None,
            activity_type=request.POST.get('activity_type'),
            activity_duration=request.POST.get('activity_duration') or None,
            symptoms=symptoms_str,
            notes=request.POST.get('notes', '')
        )

        messages.success(request, 'Glucose record saved successfully!')
        return redirect('glucose')

    context = {
        'today_date': date.today().isoformat(),
        'current_time': datetime.now().strftime('%H:%M'),
    }

    return render(request, 'add_record.html', context)


@login_required
def glucose_page(request):

    records = GlucoseRecord.objects.filter(user=request.user).order_by('-date', '-time')

    total_records = records.count()

    if total_records > 0:

        avg_glucose = sum(r.glucose_level for r in records) / total_records
        estimated_a1c = (avg_glucose + 46.7) / 28.7

        high_count = sum(1 for r in records if r.get_glucose_category() == 'high')
        low_count = sum(1 for r in records if r.get_glucose_category() == 'low')
        normal_count = sum(1 for r in records if r.get_glucose_category() == 'normal')
        prediabetes_count = sum(1 for r in records if r.get_glucose_category() == 'prediabetes')

    else:

        avg_glucose = 0
        estimated_a1c = 0
        high_count = low_count = normal_count = prediabetes_count = 0

    context = {
        'glucose_records': records,
        'avg_glucose': round(avg_glucose, 1),
        'estimated_a1c': round(estimated_a1c, 1),
        'high_count': high_count,
        'low_count': low_count,
        'normal_count': normal_count,
        'prediabetes_count': prediabetes_count,
        'total_records': total_records
    }

    return render(request, 'glucose.html', context)


# ---------------- BLOOD PRESSURE ---------------- #

@login_required
def add_bp(request):

    if request.method == "POST":

        BPRecord.objects.create(
            user=request.user,
            systolic=request.POST.get('systolic'),
            diastolic=request.POST.get('diastolic'),
            pulse=request.POST.get('pulse') or None,
            date=request.POST.get('date'),
            notes=request.POST.get('notes', '')
        )

        messages.success(request, 'Blood pressure record added successfully!')
        return redirect('bp')

    return render(request, "add_bp.html", {'today_date': date.today().isoformat()})


@login_required
def bp_page(request):

    records = BPRecord.objects.filter(user=request.user).order_by('-date')

    total_records = records.count()

    if total_records > 0:

        avg_systolic = sum(r.systolic for r in records) / total_records
        avg_diastolic = sum(r.diastolic for r in records) / total_records

    else:

        avg_systolic = avg_diastolic = 0

    context = {
        'bp_records': records,
        'avg_systolic': round(avg_systolic, 1),
        'avg_diastolic': round(avg_diastolic, 1),
        'total_records': total_records
    }

    return render(request, 'bp.html', context)


# ---------------- REMINDERS ---------------- #

@login_required
def reminder_settings(request):

    prefs, created = NotificationPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':

        prefs.email_enabled = request.POST.get('email_enabled') == 'on'
        prefs.sms_enabled = request.POST.get('sms_enabled') == 'on'
        prefs.email_address = request.POST.get('email_address', '')
        prefs.phone_number = request.POST.get('phone_number', '')
        prefs.carrier = request.POST.get('carrier', '') 

        prefs.save()

        messages.success(request, 'Notification preferences updated!')
        return redirect('reminder_settings')

    reminders = Reminder.objects.filter(user=request.user).order_by('reminder_time')

    context = {
        'prefs': prefs,
        'reminders': reminders,
        'reminder_types': Reminder.REMINDER_TYPES,
        'frequency_choices': Reminder.FREQUENCY_CHOICES,
        'today_date': date.today().isoformat(),
    }

    return render(request, 'reminder_settings.html', context)


@login_required
def add_reminder(request):
    """Add a new reminder"""
    if request.method == 'POST':
        try:
            # Get start date
            start_date_str = request.POST.get('start_date')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else date.today()
            
            # Get days of week (for weekly reminders)
            days_of_week = request.POST.get('days_of_week', '')
            
            # For one-time reminders, specific_date = start_date
            frequency = request.POST.get('frequency')
            specific_date = None
            if frequency == 'once':
                specific_date = start_date
            
            reminder = Reminder(
                user=request.user,
                reminder_type=request.POST.get('reminder_type'),
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                frequency=frequency,
                reminder_time=request.POST.get('reminder_time'),
                start_date=start_date,
                specific_date=specific_date,
                days_of_week=days_of_week,
                medication_name=request.POST.get('medication_name', ''),
                medication_dosage=request.POST.get('medication_dosage', ''),
                test_condition=request.POST.get('test_condition', ''),
                is_active=True,
                notify_in_app=True,
                notify_email=True,
                notify_sms=False,
                notify_whatsapp=False,
                override_quiet_hours=False,
            )
            reminder.save()
            
            messages.success(request, '✅ Reminder created successfully!')
            return redirect('reminder_settings')
            
        except Exception as e:
            messages.error(request, f'❌ Error creating reminder: {str(e)}')
            return redirect('reminder_settings')
    
    return redirect('reminder_settings')


@login_required
def delete_reminder(request, reminder_id):

    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.delete()

    messages.success(request, 'Reminder deleted successfully!')
    return redirect('reminder_settings')


@login_required
def toggle_reminder(request, reminder_id):

    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    reminder.is_active = not reminder.is_active
    reminder.save()

    return redirect('reminder_settings')


# ---------------- ALARMS ---------------- #

@login_required
def show_alarm(request, reminder_id):

    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    NotificationLog.objects.create(
        user=request.user,
        reminder=reminder,
        notification_type='in_app',
        title=f'Alarm: {reminder.title}',
        message='Alarm triggered',
        status='sent'
    )

    return render(request, 'reminder_alarm.html', {'reminder': reminder})


@login_required
def dismiss_alarm(request, reminder_id):

    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    messages.success(request, f'Alarm dismissed for {reminder.title}')
    return redirect('dashboard')


@login_required
def check_active_alarms(request):

    now = datetime.now()

    active = Reminder.objects.filter(
        user=request.user,
        is_active=True,
        start_date__lte=now.date(),
        reminder_time__hour=now.hour,
        reminder_time__minute=now.minute
    ).first()

    if active:
        return JsonResponse({
            'has_alarm': True,
            'reminder_id': active.id,
            'title': active.title
        })

    return JsonResponse({'has_alarm': False})


@login_required
def snooze_alarm(request, reminder_id):
    """Snooze an alarm for 5 minutes"""

    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    now = datetime.now()
    snooze_time = now + timedelta(minutes=5)

    Reminder.objects.create(
        user=request.user,
        reminder_type=reminder.reminder_type,
        title=f"SNOOZED: {reminder.title}",
        description="Snoozed reminder",
        frequency='once',
        reminder_time=snooze_time.time(),
        start_date=now.date(),
        specific_date=now.date(),
        is_active=True
    )

    reminder.is_active = False
    reminder.save()

    messages.info(request, f"Alarm snoozed until {snooze_time.strftime('%H:%M')}")

    return redirect('dashboard')


# ---------------- AI DIABETES PREDICTION ---------------- #

@login_required
def ai_prediction(request):
    return render(request, "ai_prediction.html")
<<<<<<< naveena
<<<<<<< HEAD
=======


>>>>>>> main
@login_required
def admin_dashboard(request):

    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'health_worker':
        return redirect('dashboard')

    total_users = User.objects.count()

    high_risk = GlucoseRecord.objects.filter(glucose_level__gt=250).count()

    missed_medication = GlucoseRecord.objects.filter(medication_taken=False).count()

    recent_alerts = NotificationLog.objects.all()[:10]

    context = {
        'total_users': total_users,
        'high_risk': high_risk,
        'missed_medication': missed_medication,
        'recent_alerts': recent_alerts
    }

    return render(request, 'admin_dashboard.html', context)
=======

def accessibility(request):
    return render(request, "accessibility.html")

def ai_assistant(request):
    return render(request, "ai_assistant.html")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.ai_chatbot import get_bot_response

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        reply = get_bot_response(message)
        return JsonResponse({"response": reply})
>>>>>>> 889d29d (AI assistant)
