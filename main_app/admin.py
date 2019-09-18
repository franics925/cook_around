from django.contrib import admin
from .models import Profile, Meal, Photo, Cart, Review, Entry, Transaction

class EntryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.cart.total += obj.quantity * obj.meal.price
        obj.cart.count += obj.quantity
        obj.cart.save()
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Meal)
admin.site.register(Photo)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Transaction)
admin.site.register(Entry, EntryAdmin)
