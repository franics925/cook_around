from django.contrib import admin
from .models import Profile, Meal, Photo

# Register your models here.
admin.site.register(Profile)
admin.site.register(Meal)
admin.site.register(Photo)