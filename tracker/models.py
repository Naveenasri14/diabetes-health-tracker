# tracker/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class GlucoseRecord(models.Model):
    # User Reference
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='glucose_records')
    
    # Basic Glucose Information
    glucose_level = models.FloatField(verbose_name="Glucose Level (mg/dL)")
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    
    # Reading Type Choices
    READING_TYPE_CHOICES = [
        ('fasting', 'Fasting (before breakfast)'),
        ('before_meal', 'Before Meal'),
        ('after_meal', 'After Meal'),
        ('random', 'Random'),
        ('bedtime', 'Bedtime'),
        ('night', 'Night (2-3 AM)'),
    ]
    reading_type = models.CharField(max_length=20, choices=READING_TYPE_CHOICES, default='random')
    
    # Meal Information
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('none', 'No Meal'),
    ]
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, blank=True, null=True)
    food_notes = models.TextField(blank=True, verbose_name="Food Description")
    
    # Medication / Insulin
    medication_taken = models.BooleanField(default=False)
    medicine_name = models.CharField(max_length=200, blank=True)
    insulin_dose = models.FloatField(blank=True, null=True, verbose_name="Insulin Dose (units)")
    
    # Physical Activity
    ACTIVITY_TYPE_CHOICES = [
        ('walking', 'Walking'),
        ('running', 'Running/Jogging'),
        ('yoga', 'Yoga'),
        ('gym', 'Gym/Weight Training'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('other', 'Other'),
    ]
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, blank=True, null=True)
    activity_duration = models.IntegerField(blank=True, null=True, verbose_name="Activity Duration (minutes)")
    
    # Symptoms
    SYMPTOM_CHOICES = [
        ('dizziness', 'Dizziness'),
        ('sweating', 'Sweating'),
        ('fatigue', 'Fatigue'),
        ('headache', 'Headache'),
        ('blurred_vision', 'Blurred Vision'),
        ('confusion', 'Confusion'),
        ('irritability', 'Irritability'),
        ('hunger', 'Extreme Hunger'),
        ('thirst', 'Excessive Thirst'),
        ('none', 'No Symptoms'),
    ]
    symptoms = models.CharField(max_length=100, blank=True, help_text="Comma-separated symptoms")
    
    # Additional Notes
    notes = models.TextField(blank=True, verbose_name="Additional Comments")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Glucose Record"
        verbose_name_plural = "Glucose Records"
    
    def __str__(self):
        return f"{self.user.username} - {self.glucose_level} mg/dL - {self.date} {self.time}"
    
    def get_symptoms_list(self):
        """Return symptoms as a list"""
        return self.symptoms.split(',') if self.symptoms else []
    
    def get_glucose_category(self):
        """Categorize glucose level based on reading type"""
        if self.reading_type == 'fasting':
            if self.glucose_level < 70:
                return 'low'
            elif self.glucose_level <= 100:
                return 'normal'
            elif self.glucose_level <= 125:
                return 'prediabetes'
            else:
                return 'high'
        else:  # Post-meal or random
            if self.glucose_level < 70:
                return 'low'
            elif self.glucose_level <= 140:
                return 'normal'
            elif self.glucose_level <= 199:
                return 'prediabetes'
            else:
                return 'high'

class BPRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bp_records')
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    pulse = models.IntegerField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.systolic}/{self.diastolic} - {self.date}"

class NotificationPreference(models.Model):
    """User preferences for notifications"""
    NOTIFICATION_METHODS = [
        ('in_app', 'In-App Notifications'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_prefs')
    
    # Notification methods enabled
    in_app_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=False)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=False)
    whatsapp_enabled = models.BooleanField(default=False)
    
    # Contact details
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    
    # Quiet hours
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification Preferences for {self.user.username}"

class Reminder(models.Model):
    """User-configured reminders"""
    REMINDER_TYPES = [
        ('glucose_test', 'Blood Glucose Test'),
        ('medication', 'Take Medication'),
        ('insulin', 'Insulin Injection'),
        ('meal', 'Meal Time'),
        ('exercise', 'Physical Activity'),
        ('doctor_appointment', 'Doctor Appointment'),
        ('refill', 'Prescription Refill'),
    ]
    
    FREQUENCY_CHOICES = [
        ('once', 'One Time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Timing
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    reminder_time = models.TimeField()
    days_of_week = models.CharField(max_length=50, blank=True, help_text="Comma-separated days (0-6, 0=Monday)")
    
    # For one-time reminders
    specific_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(default=timezone.now, help_text="When to start this reminder")
    
    # For medication-specific reminders
    medication_name = models.CharField(max_length=200, blank=True)
    medication_dosage = models.CharField(max_length=100, blank=True)
    
    # For glucose test reminders
    test_condition = models.CharField(max_length=50, blank=True, help_text="e.g., before_meal, after_meal, fasting")
    
    # Active status
    is_active = models.BooleanField(default=True)
    
    # Smart reminders (triggered by patterns)
    smart_reminder = models.BooleanField(default=False, help_text="Reminder based on glucose patterns")
    
    # ===== NEW FIELDS TO ADD =====
    # Notification methods for this specific reminder
    notify_in_app = models.BooleanField(default=True, help_text="Show in-app notification")
    notify_email = models.BooleanField(default=False, help_text="Send email")
    notify_sms = models.BooleanField(default=False, help_text="Send SMS")
    notify_whatsapp = models.BooleanField(default=False, help_text="Send WhatsApp")
    override_quiet_hours = models.BooleanField(default=False, help_text="Send even during quiet hours")
    # ===== END NEW FIELDS =====
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['reminder_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_reminder_type_display()} at {self.reminder_time}"

class NotificationLog(models.Model):
    """Log of sent notifications"""
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    reminder = models.ForeignKey(Reminder, on_delete=models.SET_NULL, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NotificationPreference.NOTIFICATION_METHODS)
    title = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']

class BloodSugarRecord(models.Model):
    READING_TYPE_CHOICES = [
        ('fasting', 'Fasting'),
        ('post_meal', 'Post Meal'),
        ('random', 'Random'),
        ('before_sleep', 'Before Sleep'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_type = models.CharField(max_length=20, choices=READING_TYPE_CHOICES)
    value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reading_type} - {self.value}"

# Add these new models at the end of your models.py

class VideoTutorial(models.Model):
    """Video tutorials for diabetes education"""
    VIDEO_TYPES = [
        ('insulin', 'Insulin Injection Demo'),
        ('foot_care', 'Foot Care Demo'),
        ('cooking', 'Healthy Cooking Guide'),
        ('glucose_monitoring', 'Glucose Monitoring'),
        ('exercise', 'Exercise Guide'),
    ]
    
    title = models.CharField(max_length=200)
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPES)
    youtube_url = models.URLField(help_text="YouTube video URL")
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=50, blank=True, help_text="Video duration, e.g., 5:30")
    thumbnail = models.URLField(blank=True, help_text="Thumbnail image URL")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Video Tutorial"
        verbose_name_plural = "Video Tutorials"
    
    def __str__(self):
        return self.title

class MythFact(models.Model):
    """Myth vs Fact educational content"""
    myth = models.CharField(max_length=300)
    fact = models.TextField()
    explanation = models.TextField(blank=True, help_text="Detailed explanation")
    category = models.CharField(max_length=100, blank=True, help_text="e.g., Diet, Medication, Exercise")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Myth & Fact"
        verbose_name_plural = "Myths & Facts"
    
    def __str__(self):
        return f"Myth: {self.myth[:50]}..."

class HealthTip(models.Model):
    """Audio health tips"""
    TIP_CATEGORIES = [
        ('diet', 'Diet & Nutrition'),
        ('exercise', 'Physical Activity'),
        ('medication', 'Medication'),
        ('foot_care', 'Foot Care'),
        ('glucose', 'Glucose Monitoring'),
        ('general', 'General Health'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=TIP_CATEGORIES)
    content = models.TextField(help_text="Tip content for text display")
    audio_url = models.URLField(blank=True, help_text="URL to audio file (MP3)")
    duration = models.CharField(max_length=20, blank=True, help_text="Audio duration")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Health Tip"
        verbose_name_plural = "Health Tips"
    
    def __str__(self):
        return self.title