# tracker/services/smart_reminder.py

from datetime import datetime, timedelta
from ..models import GlucoseRecord, Reminder
from .notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

class SmartReminderService:
    """Intelligent reminder system based on user patterns"""
    
    @classmethod
    def check_patterns_and_notify(cls, user):
        """Check glucose patterns and send smart notifications"""
        
        # Get recent glucose records (last 7 days)
        recent_records = GlucoseRecord.objects.filter(
            user=user,
            date__gte=datetime.now().date() - timedelta(days=7)
        ).order_by('-date', '-time')
        
        if not recent_records:
            return
        
        # Check for missed readings
        cls._check_missed_readings(user, recent_records)
        
        # Check for high/low patterns
        cls._check_glucose_patterns(user, recent_records)
        
        # Check for medication timing
        cls._check_medication_adherence(user, recent_records)
    
    @classmethod
    def _check_missed_readings(cls, user, recent_records):
        """Check if user missed expected readings based on their schedule"""
        
        # Get user's reminder schedule
        reminders = Reminder.objects.filter(
            user=user,
            reminder_type='glucose_test',
            is_active=True
        )
        
        today = datetime.now().date()
        
        for reminder in reminders:
            # Check if they have a reading for this reminder time today
            has_reading = recent_records.filter(
                date=today,
                time__hour=reminder.reminder_time.hour
            ).exists()
            
            if not has_reading and reminder.reminder_time <= datetime.now().time():
                # Send missed reading notification
                service = NotificationService(user)
                service.send_notification(
                    reminder=reminder,
                    title="Missed Glucose Reading",
                    message=f"You missed your scheduled glucose reading at {reminder.reminder_time.strftime('%I:%M %p')}. Please take a reading now."
                )
    
    @classmethod
    def _check_glucose_patterns(cls, user, recent_records):
        """Detect patterns like consistently high/low readings"""
        
        if len(recent_records) < 3:
            return
        
        # Check for three consecutive high readings
        high_count = 0
        for record in recent_records[:5]:  # Check last 5 records
            if record.get_glucose_category() in ['high', 'prediabetes']:
                high_count += 1
            else:
                break
        
        if high_count >= 3:
            service = NotificationService(user)
            service.send_notification(
                reminder=None,
                title="High Glucose Pattern Detected",
                message=f"You've had {high_count} consecutive high glucose readings. Consider consulting your healthcare provider."
            )
        
        # Check for three consecutive low readings
        low_count = 0
        for record in recent_records[:5]:
            if record.get_glucose_category() == 'low':
                low_count += 1
            else:
                break
        
        if low_count >= 3:
            service = NotificationService(user)
            service.send_notification(
                reminder=None,
                title="Low Glucose Pattern Detected",
                message=f"You've had {low_count} consecutive low glucose readings. Please review your medication or meal timing."
            )
    
    @classmethod
    def _check_medication_adherence(cls, user, recent_records):
        """Check if medication is being taken as prescribed"""
        
        # Get today's records with medication
        today_records = recent_records.filter(date=datetime.now().date())
        
        # Check if medication was recorded today
        medication_taken_today = today_records.filter(medication_taken=True).exists()
        
        # Get medication reminders
        med_reminders = Reminder.objects.filter(
            user=user,
            reminder_type='medication',
            is_active=True
        )
        
        if med_reminders.exists() and not medication_taken_today:
            # Check if it's past the reminder time
            current_time = datetime.now().time()
            for reminder in med_reminders:
                if reminder.reminder_time <= current_time:
                    service = NotificationService(user)
                    service.send_notification(
                        reminder=reminder,
                        title="Medication Reminder",
                        message=f"Don't forget to take your {reminder.medication_name or 'medication'} today."
                    )
                    break