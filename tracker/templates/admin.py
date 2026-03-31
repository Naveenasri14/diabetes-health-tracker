from django.contrib import admin
from .models import GlucoseRecord, BPRecord

admin.site.register(GlucoseRecord)
admin.site.register(BPRecord)