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