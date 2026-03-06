from django.shortcuts import render , redirect
from .models import GlucoseRecord, BPRecord
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error_message': 'Invalid username or password!'
            })
    
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard(request):
    glucose_records = GlucoseRecord.objects.filter(user=request.user).order_by('-date')
    bp_records = BPRecord.objects.filter(user=request.user).order_by('-date')

    context = {
        'glucose_records': glucose_records,
        'bp_records': bp_records
    }

    return render(request, "dashboard.html", context)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required
def add_record(request):
    if request.method == "POST":
        blood = request.POST['blood_sugar']
        meal = request.POST['meal']
        med = request.POST['medication']
        ex = request.POST['exercise']

        GlucoseRecord.objects.create(
            user=request.user,
            blood_sugar=blood,
            meal=meal,
            medication=med,
            exercise=ex
        )

        return redirect('dashboard')

    return render(request, "add_record.html")
@login_required
def add_bp(request):
    if request.method == "POST":
        systolic = request.POST['systolic']
        diastolic = request.POST['diastolic']
        pulse = request.POST['pulse']

        BPRecord.objects.create(
            user=request.user,
            systolic=systolic,
            diastolic=diastolic,
            pulse=pulse
        )

        return redirect('dashboard')

    return render(request, "add_bp.html")
@login_required
def glucose_page(request):
    records = GlucoseRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, "glucose.html", {'glucose_records': records})


@login_required
def bp_page(request):
    records = BPRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, "bp.html", {'bp_records': records})