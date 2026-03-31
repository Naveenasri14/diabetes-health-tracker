from django.urls import path
from . import views

urlpatterns = [

    # ── Auth ──────────────────────────────────────────
    path('',        views.signup,      name='home'),
    path('signup/', views.signup,      name='signup'),
    path('login/',  views.login_view,  name='login_view'),
    path('logout/', views.logout_view, name='logout'),

    # ── Role-based redirect (called after every login) ─
    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),

    # ── Role dashboards ───────────────────────────────
    path('patient/',       views.patient_dashboard,       name='patient_dashboard'),
    path('caregiver/',     views.caregiver_dashboard,     name='caregiver_dashboard'),
    path('health-worker/', views.health_worker_dashboard, name='health_worker_dashboard'),

    # ── General dashboard (fallback) ──────────────────
    path('overview/', views.dashboard, name='dashboard'),

    # ── Caregiver setup (post-login, patients only) ───
    path('add-caregiver/', views.add_caregiver, name='add_caregiver'),

    # ── Profile ───────────────────────────────────────
    path('profile/', views.profile, name='profile'),

    # ── Glucose records ───────────────────────────────
    path('add/',     views.add_record,   name='add_record'),
    path('glucose/', views.glucose_page, name='glucose'),

    # ── Blood pressure ────────────────────────────────
    path('add-bp/', views.add_bp,  name='add_bp'),
    path('bp/',     views.bp_page, name='bp'),

    # ── Reminders ─────────────────────────────────────
    path('reminder-settings/',                   views.reminder_settings, name='reminder_settings'),
    path('reminder/add/',                        views.add_reminder,      name='add_reminder'),
    path('reminder/delete/<int:reminder_id>/',   views.delete_reminder,   name='delete_reminder'),
    path('reminder/toggle/<int:reminder_id>/',   views.toggle_reminder,   name='toggle_reminder'),

    # ── Alarm system ──────────────────────────────────
    path('alarm/<int:reminder_id>/',         views.show_alarm,          name='show_alarm'),
    path('dismiss-alarm/<int:reminder_id>/', views.dismiss_alarm,       name='dismiss_alarm'),
    path('snooze-alarm/<int:reminder_id>/',  views.snooze_alarm,        name='snooze_alarm'),
    path('check-active-alarms/',             views.check_active_alarms, name='check_alarms'),

    # ── Caregiver actions (new) ───────────────────────
    path('caregiver/note/<str:patient_username>/',    views.caregiver_add_note,     name='caregiver_add_note'),
    path('caregiver/note/delete/<int:note_id>/',      views.caregiver_delete_note,  name='caregiver_delete_note'),
    path('caregiver/message/<str:patient_username>/', views.caregiver_send_message, name='caregiver_send_message'),
    path('patient/messages/',                         views.patient_messages,       name='patient_messages'),

    # ── Manage caregiver links ────────────────────────
    path('manage-links/', views.manage_links, name='manage_links'),

    # ── AI prediction ─────────────────────────────────
    path('ai-prediction/', views.ai_prediction, name='ai_prediction'),

    # ── Health worker / admin ─────────────────────────
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ── Extra pages ───────────────────────────────────
    path('accessibility/', views.accessibility, name='accessibility'),
    path('ai-assistant/',  views.ai_assistant,  name='ai_assistant'),
    path('chatbot/',       views.chatbot,        name='chatbot'),
]