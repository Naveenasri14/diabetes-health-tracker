from django.db import models
from django.contrib.auth.models import User


class GlucoseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_sugar = models.IntegerField()
    meal = models.CharField(max_length=100)
    medication = models.CharField(max_length=100)
    exercise = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_sugar}"


class BPRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    pulse = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.systolic}/{self.diastolic}"