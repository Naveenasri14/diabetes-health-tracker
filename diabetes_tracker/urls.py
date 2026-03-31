from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include tracker app URLs (this makes all existing features work)
    path('', include('tracker.urls')),
    
    # Your diet planner URLs
    path('diet-planner/', views.diet_planner_home, name='diet_planner_home'),
    path('add-diet-log/', views.add_diet_log, name='add_diet_log'),
    path('meal-plan/', views.meal_plan_view, name='meal_plan_view'),
    path('meal-plan/<str:date>/', views.meal_plan_view, name='meal_plan_view'),
    path('diet-suggestions/', views.diet_suggestions_list, name='diet_suggestions_list'),
    path('weekly-meal-plan/', views.weekly_meal_plan, name='weekly_meal_plan'),
    path('diet-statistics/', views.diet_statistics, name='diet_statistics'),
    path('get-smart-replacement/', views.get_smart_replacement, name='get_smart_replacement'),
    
    # Django login/logout
    path('accounts/', include('django.contrib.auth.urls')),
    path('activity-tracker/', views.activity_tracker, name='activity_tracker'),
path('update-steps/', views.update_steps, name='update_steps'),
path('update-water/', views.update_water, name='update_water'),
path('add-exercise-reminder/', views.add_exercise_reminder, name='add_exercise_reminder'),
path('delete-reminder/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
]