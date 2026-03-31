from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import UserProfile, Caregiver, DietSuggestion, UserDietLog, MealPlan, ActivityLog, ExerciseReminder, WaterIntake, WalkingStreak
from .forms import DietLogForm, MealPlanForm
import json


@login_required
def profile_setup(request):
    """User profile setup view"""
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
    return render(request, "profile_setup.html")


@login_required
def add_caregiver(request):
    """Add caregiver for the patient"""
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
    return render(request, "add_caregiver.html")


# ==================== DIET PLANNER VIEWS ====================

@login_required
def diet_planner_home(request):
    """Main diet planner dashboard"""
    today = timezone.now().date()
    
    # Get today's meal plan
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'total_calories': 0}
    )
    
    # Get today's diet logs
    today_logs = UserDietLog.objects.filter(
        user=request.user,
        meal_time__date=today
    ).order_by('meal_time')
    
    # Get suggestions for each meal type
    breakfast_suggestions = DietSuggestion.objects.filter(meal_type='breakfast')[:5]
    lunch_suggestions = DietSuggestion.objects.filter(meal_type='lunch')[:5]
    dinner_suggestions = DietSuggestion.objects.filter(meal_type='dinner')[:5]
    snack_suggestions = DietSuggestion.objects.filter(meal_type='snacks')[:5]
    
    # Calculate total calories consumed today
    total_calories = sum(log.calories_consumed for log in today_logs)
    
    context = {
        'meal_plan': meal_plan,
        'today_logs': today_logs,
        'total_calories': total_calories,
        'breakfast_suggestions': breakfast_suggestions,
        'lunch_suggestions': lunch_suggestions,
        'dinner_suggestions': dinner_suggestions,
        'snack_suggestions': snack_suggestions,
        'today': today,
    }
    return render(request, 'diabetes_tracker/diet_planner.html', context)


@login_required
def add_diet_log(request):
    """Add a diet log entry"""
    if request.method == 'POST':
        form = DietLogForm(request.POST)
        if form.is_valid():
            diet_log = form.save(commit=False)
            diet_log.user = request.user
            diet_log.save()
            messages.success(request, 'Diet log added successfully!')
            return redirect('diet_planner_home')
    else:
        form = DietLogForm()
    
    context = {'form': form}
    return render(request, 'diabetes_tracker/add_diet_log.html', context)


@login_required
def meal_plan_view(request, date=None):
    """View and create meal plans"""
    if date:
        selected_date = date
    else:
        selected_date = timezone.now().date()
    
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        date=selected_date
    )
    
    if request.method == 'POST':
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            # Calculate total calories
            total = 0
            if meal_plan.breakfast:
                total += meal_plan.breakfast.calories
            if meal_plan.lunch:
                total += meal_plan.lunch.calories
            if meal_plan.dinner:
                total += meal_plan.dinner.calories
            if meal_plan.snacks:
                total += meal_plan.snacks.calories
            meal_plan.total_calories = total
            meal_plan.save()
            messages.success(request, f'Meal plan for {selected_date} saved!')
            return redirect('meal_plan_view', date=selected_date)
    else:
        form = MealPlanForm(instance=meal_plan)
    
    all_suggestions = DietSuggestion.objects.all()
    
    context = {
        'form': form,
        'meal_plan': meal_plan,
        'selected_date': selected_date,
        'all_suggestions': all_suggestions,
    }
    return render(request, 'diabetes_tracker/meal_plan.html', context)


@login_required
@login_required
def diet_suggestions_list(request):
    """List all diet suggestions with filter option"""
    suggestions = DietSuggestion.objects.all().order_by('meal_type')
    
    # Check if filtering by millet-based
    filter_millet = request.GET.get('type') == 'millet'
    
    if filter_millet:
        suggestions = suggestions.filter(is_millet_based=True)
    
    # Group by meal type
    grouped_suggestions = {
        'breakfast': suggestions.filter(meal_type='breakfast'),
        'lunch': suggestions.filter(meal_type='lunch'),
        'dinner': suggestions.filter(meal_type='dinner'),
        'snacks': suggestions.filter(meal_type='snacks'),
    }
    
    context = {
        'grouped_suggestions': grouped_suggestions,
        'filter_millet': filter_millet,
        'total_count': suggestions.count()
    }
    return render(request, 'diabetes_tracker/diet_suggestions.html', context)

@login_required
@login_required
def get_smart_replacement(request):
    """API endpoint to get smart food replacements"""
    if request.method == 'GET' and request.GET.get('food_item'):
        food_item = request.GET.get('food_item').lower().strip()
        
        # Extensive replacements dictionary
        replacements = {
            'white rice': {
                'replace_with': 'Ragi (Finger Millet)',
                'reason': 'Ragi has lower glycemic index (GI: 50) vs white rice (GI: 73). Rich in calcium and fiber.',
                'suggestion': 'Replace white rice with ragi mudde, ragi kali, or mix 50% ragi with 50% rice',
                'benefits': 'Better blood sugar control, more fiber, higher calcium'
            },
            'idly': {
                'replace_with': 'Ragi Idly or Multi-millet Idly',
                'reason': 'Traditional idly spikes blood sugar. Millet idly releases energy slowly.',
                'suggestion': 'Try ragi idly or mixed millet idly for breakfast',
                'benefits': 'Sustained energy, better satiety'
            },
            'dosa': {
                'replace_with': 'Ragi Dosa or Kambu Dosa',
                'reason': 'Millet dosas have 3x more fiber than rice dosa',
                'suggestion': 'Make dosa with 50% ragi flour for crispy texture',
                'benefits': 'Keeps you full longer, better digestion'
            },
            'sugar': {
                'replace_with': 'Palm Sugar (Panam Kalkandu) or Stevia',
                'reason': 'Palm sugar has GI 35 vs refined sugar GI 65',
                'suggestion': 'Use 1-2 tsp of palm sugar instead of white sugar',
                'benefits': 'Lower glycemic impact, natural minerals'
            },
            'potato': {
                'replace_with': 'Sweet Potato or Raw Banana',
                'reason': 'Sweet potato has more fiber and lower GI',
                'suggestion': 'Use sweet potato in curries or roast with spices',
                'benefits': 'More nutrients, better blood sugar response'
            },
            'maida': {
                'replace_with': 'Whole Wheat or Ragi Flour',
                'reason': 'Maida is refined flour with no fiber',
                'suggestion': 'Use whole wheat or ragi flour for chapatis',
                'benefits': 'More fiber, better digestion'
            },
            'parotta': {
                'replace_with': 'Ragi Parotta or Multi-grain Parotta',
                'reason': 'Maida parotta causes rapid sugar spike',
                'suggestion': 'Make parotta with whole wheat and ragi mix',
                'benefits': 'Lower glycemic response'
            },
            'biryani': {
                'replace_with': 'Millet Biryani (Samai or Kambu)',
                'reason': 'Millet biryani has lower carb load',
                'suggestion': 'Try samai (little millet) biryani with vegetables',
                'benefits': 'Same taste, better nutrition'
            },
            'pongal': {
                'replace_with': 'Millet Pongal (Thinai or Kambu)',
                'reason': 'Millet pongal has more protein and fiber',
                'suggestion': 'Make ven pongal with broken wheat or kambu',
                'benefits': 'More filling, better energy release'
            }
        }
        
        # Check for partial matches
        matched = None
        for key in replacements:
            if key in food_item:
                matched = replacements[key]
                break
        
        if matched:
            return JsonResponse(matched)
        else:
            # Generate a smart response based on the food item
            return JsonResponse({
                'replace_with': 'Millet-based alternative',
                'reason': f'{food_item.title()} can be replaced with a millet version for better diabetes management. Millets have high fiber and low glycemic index.',
                'suggestion': f'Try replacing {food_item} with a millet-based option like ragi, kambu, samai, or varagu. Start with small portions and monitor your blood sugar.',
                'benefits': 'Better blood sugar control, more nutrients, sustained energy'
            })
    
    return JsonResponse({'error': 'Please enter a food item'}, status=400)

@login_required
def weekly_meal_plan(request):
    """View weekly meal plan"""
    today = timezone.now().date()
    week_dates = [today + timezone.timedelta(days=i) for i in range(7)]
    
    weekly_plans = []
    for date in week_dates:
        plan, created = MealPlan.objects.get_or_create(
            user=request.user,
            date=date,
            defaults={'total_calories': 0}
        )
        weekly_plans.append({
            'date': date,
            'plan': plan
        })
    
    context = {
        'weekly_plans': weekly_plans,
        'today': today
    }
    return render(request, 'diabetes_tracker/weekly_meal_plan.html', context)


@login_required
def diet_statistics(request):
    """View diet statistics and insights"""
    from django.db.models import Sum, Avg, Count
    from datetime import timedelta
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Weekly statistics
    weekly_logs = UserDietLog.objects.filter(
        user=request.user,
        meal_time__date__gte=week_ago
    )
    
    weekly_calories = weekly_logs.aggregate(
        total=Sum('calories_consumed'),
        avg=Avg('calories_consumed')
    )
    
    # Monthly statistics
    monthly_logs = UserDietLog.objects.filter(
        user=request.user,
        meal_time__date__gte=month_ago
    )
    
    monthly_calories = monthly_logs.aggregate(
        total=Sum('calories_consumed'),
        avg=Avg('calories_consumed')
    )
    
    # Most frequently consumed foods
    popular_foods = UserDietLog.objects.filter(
        user=request.user
    ).values('meal_name').annotate(
        count=Count('meal_name')
    ).order_by('-count')[:5]
    
    context = {
        'weekly_calories': weekly_calories,
        'monthly_calories': monthly_calories,
        'popular_foods': popular_foods,
        'total_meals_logged': monthly_logs.count(),
        'today': today
    }
    return render(request, 'diabetes_tracker/diet_statistics.html', context)


@login_required
def activity_tracker(request):
    """Main activity tracker dashboard"""
    today = timezone.now().date()
    
    # Get or create today's activity log
    activity, created = ActivityLog.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'steps': 0, 'distance_km': 0, 'calories_burned': 0, 'active_minutes': 0}
    )
    
    # Get or create walking streak
    streak, created = WalkingStreak.objects.get_or_create(
        user=request.user,
        defaults={'current_streak': 0, 'longest_streak': 0}
    )
    
    # Get water intake for today
    water, created = WaterIntake.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'glasses': 0, 'target_glasses': 8}
    )
    
    # Get exercise reminders
    reminders = ExerciseReminder.objects.filter(user=request.user, is_active=True)
    
    # Get last 7 days activity for chart
    last_7_days = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        log = ActivityLog.objects.filter(user=request.user, date=date).first()
        last_7_days.append({
            'date': date.strftime('%a'),
            'steps': log.steps if log else 0
        })
    
    context = {
        'activity': activity,
        'streak': streak,
        'water': water,
        'reminders': reminders,
        'last_7_days': last_7_days,
        'today': today,
    }
    return render(request, 'diabetes_tracker/activity_tracker.html', context)

@login_required
def update_steps(request):
    """Update daily steps"""
    if request.method == 'POST':
        steps = int(request.POST.get('steps', 0))
        today = timezone.now().date()
        
        activity, created = ActivityLog.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={'steps': 0, 'distance_km': 0, 'calories_burned': 0, 'active_minutes': 0}
        )
        
        activity.steps = steps
        activity.distance_km = round(steps * 0.000762, 2)  # Approximate
        activity.calories_burned = int(steps * 0.04)  # Approximate
        activity.save()
        
        # Update streak
        streak, created = WalkingStreak.objects.get_or_create(user=request.user)
        yesterday = today - timedelta(days=1)
        yesterday_activity = ActivityLog.objects.filter(user=request.user, date=yesterday).first()
        
        if steps >= 5000:  # Minimum steps to maintain streak
            if yesterday_activity and yesterday_activity.steps >= 5000:
                streak.current_streak += 1
            else:
                streak.current_streak = 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.last_activity_date = today
        else:
            streak.current_streak = 0
        streak.save()
        
        messages.success(request, f'Steps updated! You walked {steps} steps today! 🚶')
        return redirect('activity_tracker')
    
    return redirect('activity_tracker')

@login_required
@login_required
def update_water(request):
    """Update water intake"""
    if request.method == 'POST':
        glasses = int(request.POST.get('glasses', 0))
        today = timezone.now().date()
        
        water, created = WaterIntake.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={'glasses': 0, 'target_glasses': 8}
        )
        
        water.glasses = glasses
        water.save()
        
        # Check if AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'glasses': water.glasses,
                'target': water.target_glasses
            })
        
        messages.success(request, f'Water intake updated! {glasses}/8 glasses today 💧')
        return redirect('activity_tracker')
    
    return redirect('activity_tracker')

@login_required
def add_exercise_reminder(request):
    """Add exercise reminder"""
    if request.method == 'POST':
        reminder_time = request.POST.get('reminder_time')
        days = request.POST.getlist('days')
        days_str = ','.join(days)
        
        ExerciseReminder.objects.create(
            user=request.user,
            reminder_time=reminder_time,
            days_of_week=days_str,
            reminder_message=request.POST.get('message', 'Time for your daily exercise! 🚶')
        )
        
        messages.success(request, 'Exercise reminder added successfully! ⏰')
        return redirect('activity_tracker')
    
    return redirect('activity_tracker')

@login_required
def delete_reminder(request, reminder_id):
    """Delete exercise reminder"""
    reminder = ExerciseReminder.objects.get(id=reminder_id, user=request.user)
    reminder.delete()
    messages.success(request, 'Reminder deleted!')
    return redirect('activity_tracker')