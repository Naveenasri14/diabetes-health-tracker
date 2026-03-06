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
]