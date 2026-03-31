from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('patient',        'Patient'),
        ('caregiver',      'Caregiver'),
        ('health_worker',  'Health Worker'),
    ]

    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role   = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    region = models.CharField(max_length=100, blank=True, default='')
    phone  = models.CharField(max_length=15, blank=True, default='')
    email  = models.EmailField(blank=True, default='')
    has_skipped_caregiver = models.BooleanField(default=False)   # from old models
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_patient(self):
        return self.role == 'patient'

    def is_caregiver(self):
        return self.role == 'caregiver'

    def is_health_worker(self):
        return self.role == 'health_worker'


class CaregiverLink(models.Model):
    """
    Stores caregiver details entered by a patient.
    Caregivers do NOT need a system account — identified by name/phone/email.
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
    caregiver_name  = models.CharField(max_length=150)
    caregiver_phone = models.CharField(max_length=15)
    caregiver_email = models.EmailField()

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
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='glucose_records')
    glucose_level = models.FloatField(verbose_name="Glucose Level (mg/dL)")
    date          = models.DateField(default=timezone.now)
    time          = models.TimeField(default=timezone.now)

    READING_TYPE_CHOICES = [
        ('fasting',     'Fasting (before breakfast)'),
        ('before_meal', 'Before Meal'),
        ('after_meal',  'After Meal'),
        ('random',      'Random'),
        ('bedtime',     'Bedtime'),
        ('night',       'Night (2-3 AM)'),
    ]
    reading_type = models.CharField(max_length=20, choices=READING_TYPE_CHOICES, default='random')

    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch',     'Lunch'),
        ('dinner',    'Dinner'),
        ('snack',     'Snack'),
        ('none',      'No Meal'),
    ]
    meal_type  = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, blank=True, null=True)
    food_notes = models.TextField(blank=True)

    medication_taken = models.BooleanField(default=False)
    medicine_name    = models.CharField(max_length=200, blank=True)
    insulin_dose     = models.FloatField(blank=True, null=True)

    ACTIVITY_TYPE_CHOICES = [
        ('walking',  'Walking'),
        ('running',  'Running/Jogging'),
        ('yoga',     'Yoga'),
        ('gym',      'Gym/Weight Training'),
        ('cycling',  'Cycling'),
        ('swimming', 'Swimming'),
        ('other',    'Other'),
    ]
    activity_type     = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, blank=True, null=True)
    activity_duration = models.IntegerField(blank=True, null=True)
    symptoms          = models.CharField(max_length=200, blank=True)
    notes             = models.TextField(blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.glucose_level} mg/dL on {self.date}"

    def get_symptoms_list(self):
        return self.symptoms.split(',') if self.symptoms else []

    def get_glucose_category(self):
        if self.reading_type == 'fasting':
            if self.glucose_level < 70:    return 'low'
            elif self.glucose_level <= 100: return 'normal'
            elif self.glucose_level <= 125: return 'prediabetes'
            else:                           return 'high'
        else:
            if self.glucose_level < 70:    return 'low'
            elif self.glucose_level <= 140: return 'normal'
            elif self.glucose_level <= 199: return 'prediabetes'
            else:                           return 'high'


class BPRecord(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bp_records')
    systolic  = models.IntegerField()
    diastolic = models.IntegerField()
    pulse     = models.IntegerField(blank=True, null=True)
    date      = models.DateField(default=timezone.now)
    notes     = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.systolic}/{self.diastolic}"


class NotificationPreference(models.Model):
    CARRIER_CHOICES = [
        ('airtel', 'Airtel'),
        ('jio',    'Jio'),
        ('vi',     'Vi (Vodafone Idea)'),
        ('bsnl',   'BSNL'),
        ('other',  'Other'),
    ]

    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_prefs')
    in_app_enabled   = models.BooleanField(default=True)
    email_enabled    = models.BooleanField(default=False)
    sms_enabled      = models.BooleanField(default=False)
    phone_number     = models.CharField(max_length=20, blank=True)
    carrier          = models.CharField(max_length=20, choices=CARRIER_CHOICES, blank=True)  # from old
    whatsapp_number  = models.CharField(max_length=20, blank=True)                           # from old
    email_address    = models.EmailField(blank=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end   = models.TimeField(null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification Preferences for {self.user.username}"


class Reminder(models.Model):
    REMINDER_TYPES = [
        ('glucose_test',       'Blood Glucose Test'),
        ('medication',         'Take Medication'),
        ('insulin',            'Insulin Injection'),
        ('meal',               'Meal Time'),
        ('exercise',           'Physical Activity'),
        ('doctor_appointment', 'Doctor Appointment'),
        ('refill',             'Prescription Refill'),
    ]
    FREQUENCY_CHOICES = [
        ('once',   'One Time'),
        ('daily',  'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]

    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    reminder_type     = models.CharField(max_length=20, choices=REMINDER_TYPES)
    title             = models.CharField(max_length=200)
    description       = models.TextField(blank=True)
    frequency         = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    reminder_time     = models.TimeField()
    days_of_week      = models.CharField(max_length=50, blank=True)
    specific_date     = models.DateField(null=True, blank=True)
    start_date        = models.DateField(default=timezone.now)
    medication_name   = models.CharField(max_length=200, blank=True)
    medication_dosage = models.CharField(max_length=100, blank=True)
    is_active         = models.BooleanField(default=True)
    notify_in_app     = models.BooleanField(default=True)
    notify_email      = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['reminder_time']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationLog(models.Model):
    STATUS_CHOICES = [
        ('sent',    'Sent'),
        ('failed',  'Failed'),
        ('pending', 'Pending'),
    ]

    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    reminder          = models.ForeignKey(Reminder, on_delete=models.SET_NULL, null=True, blank=True)
    notification_type = models.CharField(max_length=20)
    title             = models.CharField(max_length=200)
    message           = models.TextField()
    status            = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message     = models.TextField(blank=True)
    sent_at           = models.DateTimeField(auto_now_add=True)

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
    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.status}"


# ──────────────────────────────────────────
# CAREGIVER NOTES  (new models)
# ──────────────────────────────────────────

class CaregiverNote(models.Model):
    """Caregiver writes notes about a patient (visible to caregiver only)."""
    caregiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='notes_written'
    )
    patient = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='caregiver_notes'
    )
    note       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
<<<<<<< HEAD
        return f"Note by {self.caregiver.user.username} for {self.patient.user.username}"


# ──────────────────────────────────────────
# CAREGIVER → PATIENT ALERTS / MESSAGES  (new models)
# ──────────────────────────────────────────

class PatientAlert(models.Model):
    """
    In-app alert sent FROM caregiver TO patient.
    Patient sees this as a notification on their dashboard.
    """
    ALERT_TYPE_CHOICES = [
        ('check_sugar',   '🩸 Please check your blood sugar'),
        ('take_medicine', '💊 Please take your medicine'),
        ('drink_water',   '💧 Please drink water'),
        ('call_me',       '📞 Please call me'),
        ('see_doctor',    '🏥 Please visit a doctor'),
        ('emergency',     '🚨 Emergency – contact me immediately'),
        ('custom',        '✏️ Custom message'),
    ]
    READ_STATUS = [
        ('unread', 'Unread'),
        ('read',   'Read'),
    ]

    sender   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_alerts')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_alerts')
    alert_type     = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    custom_message = models.TextField(blank=True)
    status         = models.CharField(max_length=10, choices=READ_STATUS, default='unread')
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_message(self):
        if self.alert_type == 'custom':
            return self.custom_message
        return dict(self.ALERT_TYPE_CHOICES).get(self.alert_type, '')

    def __str__(self):
        return f"Alert from {self.sender.user.username} to {self.receiver.user.username}"


class CaregiverMessage(models.Model):
    """
    A quick message/alert sent by caregiver to patient.
    Shows up in the patient's notification feed.
    """
    MESSAGE_TYPES = [
        ('check_glucose', '🩸 Please check your glucose'),
        ('take_medicine', '💊 Please take your medicine'),
        ('drink_water',   '💧 Please drink water'),
        ('rest',          '🛏 Please rest'),
        ('see_doctor',    '🏥 Please see a doctor soon'),
        ('custom',        '📝 Custom message'),
    ]

    caregiver    = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages_sent')
    patient      = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='caregiver_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='check_glucose')
    custom_text  = models.TextField(blank=True)
    is_read      = models.BooleanField(default=False)
    sent_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def get_text(self):
        if self.message_type == 'custom':
            return self.custom_text
        return dict(self.MESSAGE_TYPES).get(self.message_type, self.message_type)

    def __str__(self):
        return f"{self.caregiver.user.username} → {self.patient.user.username}: {self.message_type}"
=======
        return f"{self.user.username} - {self.role}"
<<<<<<< HEAD
=======


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
>>>>>>> 22dfaf9a239c6f781a0179939b2ffb1550acf667
>>>>>>> 2d864a4c1c37a5fae0bd14b870b797c1ed3eff05
