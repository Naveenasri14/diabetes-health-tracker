from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add_record, name='add_record'),
    path('add-bp/', views.add_bp, name='add_bp'), 
    path('glucose/', views.glucose_page, name='glucose'),
    path('bp/', views.bp_page, name='bp'),
    # Add this line for reminders
    path('reminder-settings/', views.reminder_settings, name='reminder_settings'),
    path('reminder/add/', views.add_reminder, name='add_reminder'),
    path('reminder/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('reminder/toggle/<int:reminder_id>/', views.toggle_reminder, name='toggle_reminder'),
    path('alarm/<int:reminder_id>/', views.show_alarm, name='show_alarm'),
path('dismiss-alarm/<int:reminder_id>/', views.dismiss_alarm, name='dismiss_alarm'),
path('snooze-alarm/<int:reminder_id>/', views.snooze_alarm, name='snooze_alarm'),
path('check-active-alarms/', views.check_active_alarms, name='check_alarms'),
path('profile/', views.profile, name='profile'),
]
