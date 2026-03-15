from django.shortcuts import render , redirect , get_object_or_404
from .models import GlucoseRecord, BPRecord , NotificationPreference, Reminder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date, timedelta
from datetime import datetime, date
import json
from .models import NotificationPreference, Reminder
from django.contrib import messages
from django.http import JsonResponse

@login_required
def reminder_settings(request):
    """Manage notification preferences and reminders"""
    
    # Get or create notification preferences
    prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update preferences
        prefs.in_app_enabled = request.POST.get('in_app_enabled') == 'on'
        prefs.email_enabled = request.POST.get('email_enabled') == 'on'
        prefs.sms_enabled = request.POST.get('sms_enabled') == 'on'
        prefs.push_enabled = request.POST.get('push_enabled') == 'on'
        prefs.whatsapp_enabled = request.POST.get('whatsapp_enabled') == 'on'
        
        prefs.phone_number = request.POST.get('phone_number', '')
        prefs.whatsapp_number = request.POST.get('whatsapp_number', '')
        prefs.email_address = request.POST.get('email_address', '')
        
        # Quiet hours
        if request.POST.get('quiet_hours_start'):
            prefs.quiet_hours_start = request.POST.get('quiet_hours_start')
        if request.POST.get('quiet_hours_end'):
            prefs.quiet_hours_end = request.POST.get('quiet_hours_end')
        
        prefs.save()
        messages.success(request, 'Notification preferences updated!')
        return redirect('reminder_settings')
    
    # Get user's reminders
    reminders = Reminder.objects.filter(user=request.user).order_by('reminder_time')
    
    # Get today's date for the form
    today_date = date.today().isoformat()
    
    context = {
        'prefs': prefs,
        'reminders': reminders,
        'reminder_types': Reminder.REMINDER_TYPES,
        'frequency_choices': Reminder.FREQUENCY_CHOICES,
        'today_date': today_date,  # This is now properly added
    }
    return render(request, 'reminder_settings.html', context)


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
@login_required
def dashboard(request):
    glucose_records = GlucoseRecord.objects.filter(user=request.user).order_by('-date')
    bp_records = BPRecord.objects.filter(user=request.user).order_by('-date')

    context = {
        'glucose_records': glucose_records,
        'bp_records': bp_records
    }

    return render(request, "dashboard.html", context)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})




@login_required
def add_record(request):
    """Enhanced view for adding glucose records"""
    
    if request.method == 'POST':
        # Handle symptoms (multiple select)
        symptoms = request.POST.getlist('symptoms')
        symptoms_str = ','.join(symptoms) if symptoms else ''
        
        # Create new glucose record
        record = GlucoseRecord(
            user=request.user,
            glucose_level=request.POST.get('glucose_level'),
            date=request.POST.get('date') or date.today(),
            time=request.POST.get('time') or datetime.now().time(),
            reading_type=request.POST.get('reading_type'),
            meal_type=request.POST.get('meal_type'),
            food_notes=request.POST.get('food_notes', ''),
            medication_taken=request.POST.get('medication_taken') == 'on',
            medicine_name=request.POST.get('medicine_name', ''),
            insulin_dose=request.POST.get('insulin_dose') if request.POST.get('insulin_dose') else None,
            activity_type=request.POST.get('activity_type'),
            activity_duration=request.POST.get('activity_duration') if request.POST.get('activity_duration') else None,
            symptoms=symptoms_str,
            notes=request.POST.get('notes', '')
        )
        record.save()
        
        messages.success(request, 'Glucose record saved successfully!')
        return redirect('glucose')
    
    # GET request - show form with today's date and current time
    context = {
        'today_date': date.today().isoformat(),
        'current_time': datetime.now().strftime('%H:%M'),
    }
    return render(request, 'add_record.html', context)



@login_required
def add_bp(request):
    if request.method == "POST":
        systolic = request.POST.get('systolic')
        diastolic = request.POST.get('diastolic')
        pulse = request.POST.get('pulse')
        record_date = request.POST.get('date')
        notes = request.POST.get('notes', '')
        
        # Validate required fields
        if not systolic or not diastolic or not record_date:
            messages.error(request, 'Please fill in all required fields!')
            return render(request, "add_bp.html", {'today_date': date.today().isoformat()})
        
        BPRecord.objects.create(
            user=request.user,
            systolic=systolic,
            diastolic=diastolic,
            pulse=pulse if pulse else "0",
            date=record_date,
            notes=notes
        )
        
        messages.success(request, 'Blood pressure record added successfully!')
        return redirect('bp')
    
    return render(request, "add_bp.html", {'today_date': date.today().isoformat()})

@login_required
def glucose_page(request):
    records = GlucoseRecord.objects.filter(user=request.user).order_by('-date', '-time')
    
    # Calculate statistics
    total_records = records.count()
    if total_records > 0:
        avg_glucose = sum(r.glucose_level for r in records) / total_records
        high_count = sum(1 for r in records if r.get_glucose_category() == 'high')
        low_count = sum(1 for r in records if r.get_glucose_category() == 'low')
        normal_count = sum(1 for r in records if r.get_glucose_category() == 'normal')
        prediabetes_count = sum(1 for r in records if r.get_glucose_category() == 'prediabetes')
        
        # Calculate estimated A1C (average glucose to A1C conversion)
        estimated_a1c = (avg_glucose + 46.7) / 28.7
        
        # Get today's reading
        today = datetime.now().date()
        today_record = records.filter(date=today).first()
        today_reading = today_record.glucose_level if today_record else None
        today_category = today_record.get_glucose_category() if today_record else None
        
        # Calculate in-range percentage
        in_range = normal_count
        in_range_percent = round((in_range / total_records) * 100, 1)
        
        # Medication percentage
        med_count = sum(1 for r in records if r.medication_taken)
        medication_percent = round((med_count / total_records) * 100, 1) if total_records > 0 else 0
        
        # Prepare chart data (last 30 days)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_records = records.filter(date__gte=thirty_days_ago).order_by('date', 'time')
        
        chart_labels = []
        chart_values = []
        chart_types = []
        
        # Group by date to avoid too many points
        daily_readings = {}
        for record in recent_records:
            date_str = record.date.strftime('%m/%d')
            if date_str not in daily_readings:
                daily_readings[date_str] = {
                    'values': [],
                    'types': []
                }
            daily_readings[date_str]['values'].append(record.glucose_level)
            daily_readings[date_str]['types'].append(record.get_glucose_category())
        
        # Take average for each day
        for date_str, data in daily_readings.items():
            chart_labels.append(date_str)
            chart_values.append(round(sum(data['values']) / len(data['values']), 1))
            # Use the most common category for that day
            chart_types.append(max(set(data['types']), key=data['types'].count))
    else:
        avg_glucose = high_count = low_count = normal_count = prediabetes_count = 0
        estimated_a1c = 0
        today_reading = None
        today_category = None
        in_range_percent = 0
        medication_percent = 0
        chart_labels = []
        chart_values = []
        chart_types = []
    
    context = {
        'glucose_records': records,
        'avg_glucose': round(avg_glucose, 1),
        'high_count': high_count,
        'low_count': low_count,
        'normal_count': normal_count,
        'prediabetes_count': prediabetes_count,
        'total_records': total_records,
        'estimated_a1c': round(estimated_a1c, 1),
        'today_reading': today_reading,
        'today_category': today_category,
        'in_range_percent': in_range_percent,
        'medication_percent': medication_percent,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'chart_types': json.dumps(chart_types),
        'best_time': 'morning',  # You can calculate this from data
        'meal_impact': 40,  # You can calculate this from data
    }
    return render(request, 'glucose.html', context)

@login_required
def bp_page(request):
    records = BPRecord.objects.filter(user=request.user).order_by('-date')
    
    # Calculate statistics
    total_records = records.count()
    if total_records > 0:
        avg_systolic = sum(r.systolic for r in records) / total_records
        avg_diastolic = sum(r.diastolic for r in records) / total_records
        pulse_records = [r.pulse for r in records if r.pulse]
        avg_pulse = sum(pulse_records) / len(pulse_records) if pulse_records else 0
        
        # Count readings this month
        current_month = datetime.now().month
        monthly_count = records.filter(date__month=current_month).count()
        
        # Determine BP status
        if avg_systolic < 120:
            bp_status = 'normal'
        elif avg_systolic < 130:
            bp_status = 'elevated'
        else:
            bp_status = 'high'
        
        # Pulse status
        if avg_pulse < 60:
            pulse_status = 'low (athletic)'
        elif avg_pulse < 100:
            pulse_status = 'normal'
        else:
            pulse_status = 'elevated'
        
        # Prepare chart data (last 30 days)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_records = records.filter(date__gte=thirty_days_ago).order_by('date')
        
        chart_labels = []
        systolic_data = []
        diastolic_data = []
        
        for record in recent_records:
            chart_labels.append(record.date.strftime('%m/%d'))
            systolic_data.append(record.systolic)
            diastolic_data.append(record.diastolic)
    else:
        avg_systolic = avg_diastolic = avg_pulse = 0
        monthly_count = 0
        bp_status = 'unknown'
        pulse_status = 'unknown'
        chart_labels = []
        systolic_data = []
        diastolic_data = []
    
    context = {
        'bp_records': records,
        'avg_systolic': round(avg_systolic, 1),
        'avg_diastolic': round(avg_diastolic, 1),
        'avg_pulse': round(avg_pulse, 1),
        'total_records': total_records,
        'monthly_count': monthly_count,
        'bp_status': bp_status,
        'pulse_status': pulse_status,
        'chart_labels': json.dumps(chart_labels),
        'systolic_data': json.dumps(systolic_data),
        'diastolic_data': json.dumps(diastolic_data),
        'best_time': 'morning',  # You can calculate this
    }
    return render(request, 'bp.html', context)


@login_required
def add_reminder(request):
    """Add a new alarm"""
    
    if request.method == 'POST':
        try:
            # Get days of week as comma-separated string
            days_list = request.POST.getlist('days_of_week')
            days_of_week = ','.join(days_list) if days_list else ''
            
            # Get start date from form
            start_date_str = request.POST.get('start_date')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else date.today()
            
            # Create the alarm (SIMPLIFIED - no notification options)
            reminder = Reminder(
                user=request.user,
                reminder_type=request.POST.get('reminder_type'),
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                frequency=request.POST.get('frequency'),
                reminder_time=request.POST.get('reminder_time'),
                start_date=start_date,
                days_of_week=days_of_week,
                specific_date=request.POST.get('specific_date') if request.POST.get('specific_date') else None,
                medication_name=request.POST.get('medication_name', ''),
                medication_dosage=request.POST.get('medication_dosage', ''),
                test_condition=request.POST.get('test_condition', ''),
                is_active=True,
                # All notification fields set to False by default
                notify_in_app=False,
                notify_email=False,
                notify_sms=False,
                notify_whatsapp=False,
                override_quiet_hours=False,
            )
            reminder.save()
            
            messages.success(request, '✅ Alarm created successfully!')
            return redirect('reminder_settings')
            
        except Exception as e:
            messages.error(request, f'❌ Error creating alarm: {str(e)}')
            return redirect('reminder_settings')
    
    return redirect('reminder_settings')

@login_required
def delete_reminder(request, reminder_id):
    """Delete a reminder"""
    try:
        reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
        reminder.delete()
        messages.success(request, '✅ Reminder deleted successfully!')
    except Exception as e:
        messages.error(request, f'❌ Error deleting reminder: {str(e)}')
    
    return redirect('reminder_settings')

@login_required
def toggle_reminder(request, reminder_id):
    """Toggle reminder active status"""
    try:
        reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
        reminder.is_active = not reminder.is_active
        reminder.save()
        status = "activated" if reminder.is_active else "deactivated"
        messages.success(request, f'✅ Reminder {status} successfully!')
    except Exception as e:
        messages.error(request, f'❌ Error toggling reminder: {str(e)}')
    
    return redirect('reminder_settings')



from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import NotificationLog

@login_required
def show_alarm(request, reminder_id):
    """Show the alarm page for a reminder"""
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    
    # Log that alarm was shown
    NotificationLog.objects.create(
        user=request.user,
        reminder=reminder,
        notification_type='in_app',
        title=f'🔔 ALARM: {reminder.title}',
        message='Alarm triggered',
        status='sent'
    )
    
    return render(request, 'reminder_alarm.html', {'reminder': reminder})

@login_required
def dismiss_alarm(request, reminder_id):
    """Dismiss an alarm"""
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    
    # Log dismissal
    NotificationLog.objects.create(
        user=request.user,
        reminder=reminder,
        notification_type='in_app',
        title=f'✅ Dismissed: {reminder.title}',
        message='Alarm dismissed by user',
        status='sent'
    )
    
    messages.success(request, f'✅ Alarm dismissed for {reminder.title}')
    return redirect('dashboard')

@login_required
def snooze_alarm(request, reminder_id):
    """Snooze an alarm for 5 minutes"""
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    
    # Create a snoozed reminder for 5 minutes later
    now = datetime.now()
    snooze_time = now + timedelta(minutes=5)
    
    snoozed = Reminder.objects.create(
        user=request.user,
        reminder_type=reminder.reminder_type,
        title=f'⏰ SNOOZED: {reminder.title}',
        description=f'Snoozed from {now.strftime("%H:%M")}',
        frequency='once',
        reminder_time=snooze_time.time(),
        start_date=now.date(),
        specific_date=now.date(),
        is_active=True,
        notify_in_app=True,
        notify_email=False,
        notify_sms=False,
        notify_whatsapp=False,
        override_quiet_hours=True,
        test_condition=reminder.test_condition,
        medication_name=reminder.medication_name,
        medication_dosage=reminder.medication_dosage,
    )
    
    # Deactivate the original reminder
    reminder.is_active = False
    reminder.save()
    
    messages.info(request, f'⏰ Alarm snoozed until {snooze_time.strftime("%I:%M %p")}')
    return redirect('dashboard')

@login_required
def check_active_alarms(request):
    """Check if there are any active alarms for the user"""
    
    now = datetime.now()
    current_time = now.time()
    current_date = now.date()
    
    # Check for alarms in the last 2 minutes
    time_window_start = (now - timedelta(minutes=2)).time()
    
    active = Reminder.objects.filter(
        user=request.user,
        is_active=True,
        start_date__lte=current_date,
        reminder_time__gte=time_window_start,
        reminder_time__lte=current_time,
    ).first()
    
    if active:
        return JsonResponse({
            'has_alarm': True,
            'reminder_id': active.id,
            'title': active.title,
            'sound': True  # Tell browser to play sound
        })
    return JsonResponse({'has_alarm': False, 'sound': False})
@login_required
def check_active_alarms(request):
    """Check if there are any active alarms for the user"""
    now = datetime.now()
    current_time = now.time()
    current_date = now.date()
    
    # Check for any due reminders in the last minute
    time_window_start = (now - timedelta(minutes=1)).time()
    
    active = Reminder.objects.filter(
        user=request.user,
        is_active=True,
        start_date__lte=current_date,
        reminder_time__gte=time_window_start,
        reminder_time__lte=current_time,
    ).first()
    
    if active:
        return JsonResponse({
            'has_alarm': True,
            'reminder_id': active.id,
            'title': active.title
        })
    return JsonResponse({'has_alarm': False})

@login_required
def reminder_settings(request):
    """Manage notification preferences and reminders"""
    
    # Get or create notification preferences
    prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update preferences
        prefs.email_enabled = request.POST.get('email_enabled') == 'on'
        prefs.sms_enabled = request.POST.get('sms_enabled') == 'on'
        prefs.email_address = request.POST.get('email_address', '')
        prefs.phone_number = request.POST.get('phone_number', '')
        
        prefs.save()
        messages.success(request, '✅ Notification preferences updated!')
        return redirect('reminder_settings')
    
    # Get user's reminders
    reminders = Reminder.objects.filter(user=request.user).order_by('reminder_time')
    
    # Get today's date for the form
    today_date = date.today().isoformat()
    
    context = {
        'prefs': prefs,
        'reminders': reminders,
        'reminder_types': Reminder.REMINDER_TYPES,
        'frequency_choices': Reminder.FREQUENCY_CHOICES,
        'today_date': today_date,
    }
    return render(request, 'reminder_settings.html', context)