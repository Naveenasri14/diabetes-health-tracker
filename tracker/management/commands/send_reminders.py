from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from tracker.models import Reminder, NotificationLog
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
        
        # Debug: Show current time
        self.stdout.write(f"Current time: {current_time}")
        self.stdout.write(f"Current hour: {current_time.hour}, minute: {current_time.minute}")
        self.stdout.write(f"Current date: {current_date}")
        self.stdout.write("-" * 40)
        
        # Get all active reminders
        reminders = Reminder.objects.filter(is_active=True)
        self.stdout.write(f"Found {reminders.count()} active reminders")
        alarms_triggered = 0
        
        for reminder in reminders:
            self.stdout.write(f"\n--- Processing reminder: {reminder.title} ---")
            self.stdout.write(f"Reminder time: {reminder.reminder_time}")
            self.stdout.write(f"Reminder start_date: {reminder.start_date}")
            self.stdout.write(f"Reminder specific_date: {reminder.specific_date}")
            self.stdout.write(f"Reminder frequency: {reminder.frequency}")
            
            # Check if reminder has started
            if reminder.start_date > current_date:
                self.stdout.write(f"⏰ {reminder.title} - Start date in future ({reminder.start_date} > {current_date})")
                continue
            
            should_trigger = False
            
            # Check frequency and time
            if reminder.frequency == 'once':
                self.stdout.write(f"Frequency: once - checking specific_date...")
                if reminder.specific_date == current_date:
                    self.stdout.write(f"✅ specific_date matches! Checking time...")
                    if self._time_matches(reminder.reminder_time, current_time):
                        should_trigger = True
                        reminder.is_active = False
                        reminder.save()
                        self.stdout.write(f"✅ {reminder.title} - Triggered (one-time, now inactive)")
                    else:
                        self.stdout.write(f"❌ Time did NOT match")
                else:
                    self.stdout.write(f"❌ specific_date ({reminder.specific_date}) != current_date ({current_date})")
            
            elif reminder.frequency == 'daily':
                self.stdout.write(f"Frequency: daily - checking time...")
                if self._time_matches(reminder.reminder_time, current_time):
                    should_trigger = True
                    self.stdout.write(f"✅ {reminder.title} - Triggered (daily)")
                else:
                    self.stdout.write(f"❌ Time did NOT match for daily alarm")
            
            elif reminder.frequency == 'weekly':
                self.stdout.write(f"Frequency: weekly - checking...")
                if reminder.days_of_week:
                    days = [int(d.strip()) for d in reminder.days_of_week.split(',')]
                    self.stdout.write(f"  Days of week: {days}, current weekday: {current_weekday}")
                    if current_weekday in days and self._time_matches(reminder.reminder_time, current_time):
                        should_trigger = True
                        self.stdout.write(f"✅ {reminder.title} - Triggered (weekly)")
                    else:
                        self.stdout.write(f"❌ Not triggered - weekday not in list or time didn't match")
                else:
                    self.stdout.write(f"⚠️ No days_of_week set for weekly alarm")
            
            if should_trigger:
                self._send_email(reminder)
                alarms_triggered += 1
            else:
                self.stdout.write(f"⏰ {reminder.title} at {reminder.reminder_time} - Not triggered")
        
        self.stdout.write(self.style.SUCCESS(f'✅ Completed. Triggered {alarms_triggered} alarms.'))
    
    def _time_matches(self, reminder_time, current_time, tolerance=2):
        """Check if reminder time matches current time"""
        
        # Convert to minutes since midnight
        reminder_total = reminder_time.hour * 60 + reminder_time.minute
        current_total = current_time.hour * 60 + current_time.minute
        
        self.stdout.write(f"   🔍 COMPARING: Reminder {reminder_time.hour:02d}:{reminder_time.minute:02d} ({reminder_total}) vs Current {current_time.hour:02d}:{current_time.minute:02d} ({current_total})")
        
        # ALWAYS trigger if we're in the same minute
        if reminder_time.hour == current_time.hour and reminder_time.minute == current_time.minute:
            self.stdout.write(f"   ✅ SAME MINUTE! TRIGGERING!")
            return True
        
        # Also trigger if current time is within tolerance minutes after
        diff = current_total - reminder_total
        if 0 <= diff <= tolerance:
            self.stdout.write(f"   ✅ WITHIN {diff} MINUTES AFTER! TRIGGERING!")
            return True
        
        self.stdout.write(f"   ❌ NOT TRIGGERING (diff={diff} minutes)")
        return False
    
    def _send_email(self, reminder):
        """Send email alert"""
        
        # Get user's email from preferences
        if hasattr(reminder.user, 'notification_prefs'):
            prefs = reminder.user.notification_prefs
            recipient = prefs.email_address
        else:
            recipient = reminder.user.email
        
        if not recipient:
            self.stdout.write(f"⚠️ No email address for {reminder.user.username}")
            return
        
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
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Email failed: {e}"))