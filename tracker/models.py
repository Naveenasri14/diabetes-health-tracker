from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GlucoseRecord(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='glucose_records')

    glucose_level = models.FloatField(verbose_name="Glucose Level (mg/dL)")
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    READING_TYPE_CHOICES = [
        ('fasting', 'Fasting (before breakfast)'),
        ('before_meal', 'Before Meal'),
        ('after_meal', 'After Meal'),
        ('random', 'Random'),
        ('bedtime', 'Bedtime'),
        ('night', 'Night (2-3 AM)'),
    ]

    reading_type = models.CharField(
        max_length=20,
        choices=READING_TYPE_CHOICES,
        default='random'
    )

    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('none', 'No Meal'),
    ]

    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        blank=True,
        null=True
    )

    food_notes = models.TextField(blank=True)

    medication_taken = models.BooleanField(default=False)
    medicine_name = models.CharField(max_length=200, blank=True)
    insulin_dose = models.FloatField(blank=True, null=True)

    ACTIVITY_TYPE_CHOICES = [
        ('walking', 'Walking'),
        ('running', 'Running/Jogging'),
        ('yoga', 'Yoga'),
        ('gym', 'Gym/Weight Training'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('other', 'Other'),
    ]

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        blank=True,
        null=True
    )

    activity_duration = models.IntegerField(blank=True, null=True)

    symptoms = models.CharField(max_length=200, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.glucose_level} mg/dL"

    def get_symptoms_list(self):
        return self.symptoms.split(',') if self.symptoms else []

    def get_glucose_category(self):

        if self.reading_type == 'fasting':
            if self.glucose_level < 70:
                return 'low'
            elif self.glucose_level <= 100:
                return 'normal'
            elif self.glucose_level <= 125:
                return 'prediabetes'
            else:
                return 'high'

        else:
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
        return f"{self.user.username} - {self.systolic}/{self.diastolic}"


class NotificationPreference(models.Model):
    CARRIER_CHOICES = [
        ('airtel', 'Airtel'),
        ('jio', 'Jio'),
        ('vi', 'Vi (Vodafone Idea)'),
        ('bsnl', 'BSNL'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_prefs')

    in_app_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=False)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=False)
    whatsapp_enabled = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=20, blank=True)
    carrier = models.CharField(max_length=20, choices=CARRIER_CHOICES, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)

    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification Preferences for {self.user.username}"


class Reminder(models.Model):

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

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')

    reminder_time = models.TimeField()

    days_of_week = models.CharField(max_length=50, blank=True)

    specific_date = models.DateField(null=True, blank=True)

    start_date = models.DateField(default=timezone.now)

    medication_name = models.CharField(max_length=200, blank=True)
    medication_dosage = models.CharField(max_length=100, blank=True)

    test_condition = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)

    smart_reminder = models.BooleanField(default=False)

    notify_in_app = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=False)
    notify_sms = models.BooleanField(default=False)
    notify_whatsapp = models.BooleanField(default=False)

    override_quiet_hours = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['reminder_time']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
class NotificationLog(models.Model):

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    reminder = models.ForeignKey(Reminder, on_delete=models.SET_NULL, null=True, blank=True)

    notification_type = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    message = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    error_message = models.TextField(blank=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.status}"


# ✅ NEW MODEL (separate, NOT inside NotificationLog)
class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
        ('doctor', 'Doctor'),
        ('health_worker', 'Health Worker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    region = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    DIABETES_TYPE_CHOICES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('gestational', 'Gestational'),
        ('none', 'None/Pre-diabetic'),
    ]
    
    # Change related_name from 'profile' to 'tracker_profile'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tracker_profile')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    diabetes_type = models.CharField(max_length=20, choices=DIABETES_TYPE_CHOICES, null=True, blank=True)
    years_since_diagnosis = models.FloatField(null=True, blank=True)
    family_history = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight and self.height > 0:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None