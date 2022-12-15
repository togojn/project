from django.contrib import admin

# Register your models here.
from .models import Base, Seat, Schedule

admin.site.register(Base)
admin.site.register(Seat)
admin.site.register(Schedule)