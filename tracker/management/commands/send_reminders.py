from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from tracker.models import Reminder, NotificationLog
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send email alerts for active alarms'
    
    def handle(self, *args, **options):
        self.stdout.write('🔔 Alarm checker started...')
        
        # Get all active alarms
        reminders = Reminder.objects.filter(is_active=True)
        alarms_triggered = 0
        
        for reminder in reminders:
            self.stdout.write(f'🔔 Processing alarm: {reminder.title}')
            
            # Send email if enabled
            if hasattr(reminder.user, 'notification_prefs'):
                prefs = reminder.user.notification_prefs
                if prefs.email_enabled and prefs.email_address:
                    self._send_email(reminder, prefs.email_address)
                    alarms_triggered += 1
            
            # Deactivate one-time alarms after triggering
            if reminder.frequency == 'once':
                reminder.is_active = False
                reminder.save()
        
        self.stdout.write(self.style.SUCCESS(f'✅ Completed. Triggered {alarms_triggered} alarms.'))
    
    def _send_email(self, reminder, recipient):
        """Send email alert"""
        
        subject = f"🔔 Diabetes Tracker Alarm: {reminder.title}"
        
        message = f"""
        ⏰ ALARM TRIGGERED!
        
        {reminder.title}
        {reminder.description or ''}
        
        Time: {reminder.reminder_time.strftime('%I:%M %p')}
        Date: {reminder.start_date}
        Type: {reminder.get_reminder_type_display()}
        
        Please log in to confirm:
        http://127.0.0.1:8000/dashboard/
        
        ---
        Diabetes Tracker - Stay healthy!
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"📧 Email sent to {recipient}"))
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Email failed: {e}"))
            return False