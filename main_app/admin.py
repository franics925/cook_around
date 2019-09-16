from django.contrib import admin
from .models import Profile, Meal, Photo, Cart, Review, Entry

# Register your models here.
admin.site.register(Profile)
admin.site.register(Meal)
admin.site.register(Photo)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Entry)