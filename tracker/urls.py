from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is here
from django.urls import path
from . import views

urlpatterns = [

    # Home / Signup
    path('', views.signup, name='home'),
    path('signup/', views.signup, name='signup'),
    
    # Accounts (with /accounts/ prefix)
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    
    # Alternative direct login (optional)
    path('login/', views.login_view, name='login_alt'),
    path('logout/', views.logout_view, name='logout_alt'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Health Records
    path('add/', views.add_record, name='add_record'),
    path('add-bp/', views.add_bp, name='add_bp'),

    # Glucose and BP pages
    path('glucose/', views.glucose_page, name='glucose'),
    path('bp/', views.bp_page, name='bp'),

    # AI Prediction Page
    path('ai-prediction/', views.ai_prediction, name='ai_prediction'),

    path("accessibility/", views.accessibility, name="accessibility"),

    path("ai-assistant/", views.ai_assistant, name="ai_assistant"),

    path("chatbot/", views.chatbot, name="chatbot"),

    # Reminder Settings
    path('reminder-settings/', views.reminder_settings, name='reminder_settings'),
    path('reminder/add/', views.add_reminder, name='add_reminder'),
    path('reminder/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('reminder/toggle/<int:reminder_id>/', views.toggle_reminder, name='toggle_reminder'),

    # Alarm system
    path('alarm/<int:reminder_id>/', views.show_alarm, name='show_alarm'),
    path('dismiss-alarm/<int:reminder_id>/', views.dismiss_alarm, name='dismiss_alarm'),
    path('snooze-alarm/<int:reminder_id>/', views.snooze_alarm, name='snooze_alarm'),
    path('check-active-alarms/', views.check_active_alarms, name='check_alarms'),

    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]