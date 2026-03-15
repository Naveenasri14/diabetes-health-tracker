from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from tracker.models import Reminder, NotificationLog
from tracker.services.smart_reminder import SmartReminderService
from twilio.rest import Client
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check for due reminders and send notifications'
    
    def handle(self, *args, **options):
        self.stdout.write('🔔 Alarm checker started...')
        
        current_datetime = timezone.now()
        current_time = current_datetime.time()
        current_date = current_datetime.date()
        current_weekday = current_datetime.weekday()
        
        reminders = Reminder.objects.filter(is_active=True)
        alarms_triggered = 0
        
        for reminder in reminders:
            if reminder.start_date > current_date:
                continue
            
            should_trigger = False
            
            # Check frequency (same as before)
            if reminder.frequency == 'once':
                if reminder.specific_date == current_date:
                    if self._time_matches(reminder.reminder_time, current_time):
                        should_trigger = True
                        reminder.is_active = False
                        reminder.save()
            
            elif reminder.frequency == 'daily':
                if self._time_matches(reminder.reminder_time, current_time):
                    should_trigger = True
            
            elif reminder.frequency == 'weekly':
                if reminder.days_of_week:
                    days = [int(d.strip()) for d in reminder.days_of_week.split(',')]
                    if current_weekday in days and self._time_matches(reminder.reminder_time, current_time):
                        should_trigger = True
            
            if should_trigger:
                self._trigger_alarm(reminder)
                alarms_triggered += 1
        
        self.stdout.write(self.style.SUCCESS(f'✅ Completed. Triggered {alarms_triggered} alarms.'))
    
    def _time_matches(self, reminder_time, current_time, tolerance=1):
        reminder_minutes = reminder_time.hour * 60 + reminder_time.minute
        current_minutes = current_time.hour * 60 + current_time.minute
        return abs(reminder_minutes - current_minutes) <= tolerance
    
    # ========== ALL METHODS BELOW MUST BE INDENTED INSIDE THE CLASS ==========
    
    def _trigger_alarm(self, reminder):
        """Multi-channel alarm trigger with comprehensive debugging"""
        
        # 1. Log the alarm
        NotificationLog.objects.create(
            user=reminder.user,
            reminder=reminder,
            notification_type='in_app',
            title=f'🔔 ALARM: {reminder.title}',
            status='sent'
        )
        
        # 2. EMAIL HANDLING - WITH FULL DEBUGGING
        self.stdout.write("="*50)
        self.stdout.write("🔍 EMAIL DEBUG INFORMATION")
        self.stdout.write("="*50)
        
        # Check User model email
        self.stdout.write(f"📧 User model email: '{reminder.user.email}'")
        self.stdout.write(f"📧 User has email in model: {bool(reminder.user.email)}")
        
        # Check Notification Preferences
        if hasattr(reminder.user, 'notification_prefs'):
            prefs = reminder.user.notification_prefs
            self.stdout.write(f"📧 Preferences exist: YES")
            self.stdout.write(f"📧 Preferences email enabled: {prefs.email_enabled}")
            self.stdout.write(f"📧 Preferences email address: '{prefs.email_address}'")
            
            # Determine which email to use
            if prefs.email_enabled and prefs.email_address:
                recipient = prefs.email_address
                self.stdout.write(f"✅ Using preferences email: {recipient}")
                self._send_email(reminder, recipient)
            elif reminder.user.email:
                recipient = reminder.user.email
                self.stdout.write(f"⚠️ Preferences email not set/enabled, falling back to User model: {recipient}")
                self._send_email(reminder, recipient)
            else:
                self.stdout.write("❌ No email found in preferences or User model")
        else:
            self.stdout.write("📧 Preferences exist: NO")
            if reminder.user.email:
                recipient = reminder.user.email
                self.stdout.write(f"✅ Using User model email: {recipient}")
                self._send_email(reminder, recipient)
            else:
                self.stdout.write("❌ No email found in User model")
        
        self.stdout.write("="*50)
        
        # 3. SMS HANDLING (commented out)
        # if hasattr(reminder.user, 'notification_prefs'):
        #     phone = reminder.user.notification_prefs.phone_number
        #     if phone:
        #         self._send_sms(reminder, phone)
        
        # 4. Console output
        self.stdout.write(self.style.WARNING(f'\n🔔🔔🔔 ALARM TRIGGERED 🔔🔔🔔'))
        self.stdout.write(f'User: {reminder.user.username}')
        self.stdout.write(f'Title: {reminder.title}')
        self.stdout.write(f'Time: {reminder.reminder_time}')
        self.stdout.write('🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔\n')
    
    def _send_email(self, reminder, recipient):
        """Send email alert"""
        
        subject = f"🔔 Diabetes Tracker: {reminder.title}"
        
        message = f"""
        ⏰ ALARM TRIGGERED!
        
        {reminder.title}
        {reminder.description or ''}
        
        Time: {reminder.reminder_time.strftime('%I:%M %p')}
        Date: {reminder.start_date}
        Type: {reminder.get_reminder_type_display()}
        
        Please log in to confirm:
        http://127.0.0.1:8001/dashboard/
        """
        
        try:
            self.stdout.write(f"📧 Attempting to send email to: {recipient}")
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Email sent successfully to {recipient}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Email failed: {str(e)}"))
            self.stdout.write(self.style.ERROR(f"❌ Error type: {type(e).__name__}"))
    
    def _send_sms(self, reminder, phone):
        """Send SMS alert using Twilio"""
        
        # Short message for SMS (160 char limit)
        sms_message = f"🔔 {reminder.title} at {reminder.reminder_time.strftime('%I:%M %p')}. Log in: http://127.0.0.1:8001"
        
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            client.messages.create(
                body=sms_message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            
            self.stdout.write(f"📱 SMS sent to {phone}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ SMS failed: {e}"))
