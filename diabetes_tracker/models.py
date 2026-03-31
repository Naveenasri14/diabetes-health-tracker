from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    DIABETES_TYPES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('gestational', 'Gestational'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    age = models.IntegerField()

    gender = models.CharField(
        max_length=10
    )

    weight = models.FloatField()

    height = models.FloatField()

    blood_group = models.CharField(
        max_length=5
    )

    diabetes_type = models.CharField(
        max_length=20,
        choices=DIABETES_TYPES
    )

    years_since_diagnosis = models.IntegerField()

    family_history = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username} Profile"


class Caregiver(models.Model):

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="caregivers"
    )

    name = models.CharField(
        max_length=100
    )

    relationship = models.CharField(
        max_length=50
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    is_emergency_contact = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.name} ({self.relationship})"
    
class DietSuggestion(models.Model):
    """Model for storing diet suggestions"""
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]
    
    name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    description = models.TextField()
    ingredients = models.TextField(help_text="List of ingredients")
    preparation_method = models.TextField()
    calories = models.IntegerField(help_text="Calories per serving")
    is_millet_based = models.BooleanField(default=False)
    replaces = models.CharField(max_length=200, blank=True, help_text="What this replaces (e.g., 'white rice')")
    tamil_nadu_region = models.CharField(max_length=100, blank=True, help_text="Specific region if applicable")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserDietLog(models.Model):
    """Model for tracking user's diet choices"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet_suggestion = models.ForeignKey(DietSuggestion, on_delete=models.SET_NULL, null=True)
    meal_name = models.CharField(max_length=200)
    meal_time = models.DateTimeField(auto_now_add=True)
    portion_size = models.CharField(max_length=50, help_text="e.g., '1 cup', '2 chapatis'")
    calories_consumed = models.IntegerField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.meal_name} at {self.meal_time}"

class MealPlan(models.Model):
    """Model for daily meal plans"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    breakfast = models.ForeignKey(DietSuggestion, on_delete=models.SET_NULL, null=True, related_name='breakfast_plans')
    lunch = models.ForeignKey(DietSuggestion, on_delete=models.SET_NULL, null=True, related_name='lunch_plans')
    dinner = models.ForeignKey(DietSuggestion, on_delete=models.SET_NULL, null=True, related_name='dinner_plans')
    snacks = models.ForeignKey(DietSuggestion, on_delete=models.SET_NULL, null=True, related_name='snack_plans')
    total_calories = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
class ActivityLog(models.Model):
    """Model for tracking daily activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField(default=0)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calories_burned = models.IntegerField(default=0)
    active_minutes = models.IntegerField(default=0)
    streak_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.steps} steps"

class ExerciseReminder(models.Model):
    """Model for exercise reminders"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_time = models.TimeField()
    days_of_week = models.CharField(max_length=50, help_text="Comma separated: Mon,Tue,Wed,Thu,Fri,Sat,Sun")
    is_active = models.BooleanField(default=True)
    reminder_message = models.CharField(max_length=200, default="Time for your daily exercise! 🚶")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.reminder_time}"

class WaterIntake(models.Model):
    """Model for tracking water intake"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    glasses = models.IntegerField(default=0)
    target_glasses = models.IntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.glasses}/{self.target_glasses} glasses"

class WalkingStreak(models.Model):
    """Model for tracking walking streaks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Current: {self.current_streak}, Longest: {self.longest_streak}"