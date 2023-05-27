from django.contrib import admin
from .models import studends, Detected,staff

# Register your models here.

admin.site.register(studends)
admin.site.register(staff)
admin.site.register(Detected)