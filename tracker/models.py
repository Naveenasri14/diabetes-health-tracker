from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    region = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    has_skipped_caregiver = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_patient(self):
        return self.role == 'patient'

    def is_caregiver(self):
        return self.role == 'caregiver'


class CaregiverLink(models.Model):
    """
    Stores caregiver details entered by a patient.
    Caregivers do NOT need a system account — identified by name/phone/email.
    They receive a request and can accept or reject it.
    """
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    patient = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='caregiver_links'
    )

    # Caregiver info — no system account required
    caregiver_name  = models.CharField(max_length=150)
    caregiver_phone = models.CharField(max_length=15)
    caregiver_email = models.EmailField()

    # If the caregiver later registers, optionally link their profile
    caregiver_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patient_links'
    )

    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    linked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caregiver_name} → {self.patient.user.username} ({self.status})"


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
    reading_type = models.CharField(max_length=20, choices=READING_TYPE_CHOICES, default='random')

    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('none', 'No Meal'),
    ]
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, blank=True, null=True)
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
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, blank=True, null=True)
    activity_duration = models.IntegerField(blank=True, null=True)
    symptoms = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.glucose_level} mg/dL on {self.date}"

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_prefs')
    in_app_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=False)
    sms_enabled = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
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
    is_active = models.BooleanField(default=True)
    notify_in_app = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=False)
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