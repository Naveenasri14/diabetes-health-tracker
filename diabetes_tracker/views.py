from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Caregiver

@login_required
def profile_setup(request):
if request.method == "POST":
UserProfile.objects.create(
user=request.user,
age=request.POST.get('age'),
gender=request.POST.get('gender'),
weight=request.POST.get('weight'),
height=request.POST.get('height'),
blood_group=request.POST.get('blood_group'),
diabetes_type=request.POST.get('diabetes_type'),
years_since_diagnosis=request.POST.get('years'),
family_history=True if request.POST.get('family_history') else False
)
return redirect('dashboard')

```
return render(request, "profile_setup.html")
```

@login_required
def add_caregiver(request):
if request.method == "POST":
Caregiver.objects.create(
patient=request.user,
name=request.POST.get('name'),
relationship=request.POST.get('relationship'),
phone=request.POST.get('phone'),
email=request.POST.get('email'),
is_emergency_contact=True if request.POST.get('emergency') else False
)
return redirect('dashboard')

```
return render(request, "add_caregiver.html")
```
