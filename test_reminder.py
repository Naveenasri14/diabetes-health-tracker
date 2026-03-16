import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diabetes_tracker.settings')
django.setup()

from tracker.models import Reminder
from django.contrib.auth.models import User

your_username = 'sujatha_07'  # Change this!

try:
    user = User.objects.get(username=your_username)
    now = datetime.now()
    two_minutes_later = now + timedelta(minutes=2)
    
    reminder = Reminder.objects.create(
        user=user,
        reminder_type='glucose_test',
        title='🔥 TEST REMINDER',
        description='Test',
        frequency='once',
        reminder_time=two_minutes_later.time(),
        start_date=now.date(),
        specific_date=now.date(),
        is_active=True,
        notify_in_app=True,
        notify_email=True,
        override_quiet_hours=True,
    )
    
    print(f"✅ Created! Will trigger at {two_minutes_later.strftime('%H:%M:%S')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
