# tracker/services/notification_service.py

from django.core.mail import send_mail
from django.conf import settings
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service to handle all notification sending"""
    
    def __init__(self, user):
        self.user = user
        self.prefs = user.notification_prefs if hasattr(user, 'notification_prefs') else None
    
    def send_notification(self, reminder, title, message):
        """Send notification based on reminder-specific preferences"""
        
        from ..models import NotificationLog
        
        if not self.prefs:
            logger.warning(f"No notification preferences for user {self.user.username}")
            return
        
        # Check quiet hours (unless reminder overrides them)
        if not reminder.override_quiet_hours and self._in_quiet_hours():
            logger.info(f"In quiet hours for user {self.user.username}, skipping notification")
            return
        
        results = []
        
        # Check reminder-specific flags instead of global preferences
        if reminder.notify_in_app:
            result = self._send_in_app(reminder, title, message)
            results.append(('in_app', result))
        
        if reminder.notify_email and self.prefs.email_address:
            result = self._send_email(reminder, title, message)
            results.append(('email', result))
        
        if reminder.notify_sms and self.prefs.phone_number:
            result = self._send_sms(reminder, title, message)
            results.append(('sms', result))
        
        if reminder.notify_whatsapp and self.prefs.whatsapp_number:
            result = self._send_whatsapp(reminder, title, message)
            results.append(('whatsapp', result))
        
        return results
    
    def _in_quiet_hours(self):
        """Check if current time is within quiet hours"""
        if not self.prefs.quiet_hours_start or not self.prefs.quiet_hours_end:
            return False
        
        now = datetime.now().time()
        
        if self.prefs.quiet_hours_start <= self.prefs.quiet_hours_end:
            return self.prefs.quiet_hours_start <= now <= self.prefs.quiet_hours_end
        else:  # Overnight (e.g., 22:00 to 06:00)
            return now >= self.prefs.quiet_hours_start or now <= self.prefs.quiet_hours_end
    
    def _send_in_app(self, reminder, title, message):
        """Create in-app notification"""
        from ..models import NotificationLog
        
        try:
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='in_app',
                title=title,
                message=message,
                status='sent'
            )
            return True
        except Exception as e:
            logger.error(f"In-app notification failed: {str(e)}")
            return False
    
    def _send_email(self, reminder, title, message):
        """Send email notification"""
        from ..models import NotificationLog
        
        try:
            send_mail(
                subject=f"Diabetes Tracker: {title}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.prefs.email_address],
                fail_silently=False,
            )
            
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='email',
                title=title,
                message=message,
                status='sent'
            )
            return True
        except Exception as e:
            logger.error(f"Email notification failed: {str(e)}")
            
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='email',
                title=title,
                message=message,
                status='failed',
                error_message=str(e)
            )
            return False
    
    def _send_sms(self, reminder, title, message):
        """Send SMS notification using Twilio"""
        from ..models import NotificationLog
        
        try:
            # Configure Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Truncate message for SMS
            sms_message = f"{title}: {message}"[:160]
            
            client.messages.create(
                body=sms_message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=self.prefs.phone_number
            )
            
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='sms',
                title=title,
                message=message,
                status='sent'
            )
            return True
        except Exception as e:
            logger.error(f"SMS notification failed: {str(e)}")
            
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='sms',
                title=title,
                message=message,
                status='failed',
                error_message=str(e)
            )
            return False
    
    def _send_push(self, reminder, title, message):
        """Send push notification using Firebase Cloud Messaging"""
        from ..models import NotificationLog
        
        try:
            # This would integrate with Firebase Cloud Messaging
            # You'd need to store FCM tokens for each user's device
            
            # Placeholder for FCM integration
            # fcm.send_notification(user.fcm_token, title, message)
            
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='push',
                title=title,
                message=message,
                status='sent'
            )
            return True
        except Exception as e:
            logger.error(f"Push notification failed: {str(e)}")
            return False
    
    def _send_whatsapp(self, reminder, title, message):
        """Send WhatsApp notification using Twilio WhatsApp API"""
        from ..models import NotificationLog
        
        try:
            # Configure Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            client.messages.create(
                body=f"*{title}*\n\n{message}",
                from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
                to=f'whatsapp:{self.prefs.whatsapp_number}'
            )
            
            NotificationLog.objects.create(
                user=self.user,
                reminder=reminder,
                notification_type='whatsapp',
                title=title,
                message=message,
                status='sent'
            )
            return True
        except Exception as e:
            logger.error(f"WhatsApp notification failed: {str(e)}")
            return False