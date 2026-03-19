from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # connect tracker app
    path('', include('tracker.urls')),

    # django login/logout
    path('accounts/', include('django.contrib.auth.urls')),
]