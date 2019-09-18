from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
  user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
  chef = models.BooleanField(default=False)
  address1 = models.CharField(max_length=50, blank=True)
  address2 = models.CharField(max_length=50, null=True, blank=True)
  city = models.CharField(max_length=50, blank=True)
  state = models.CharField(max_length=30, blank=True)
  zipcode = models.IntegerField(null=True, blank=True)

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(user=instance)
  
  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Meal(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=50)
  quantity = models.IntegerField(default=1)
  price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
  chef = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('details', kwargs={'meal_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=200)
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for meal_id: {self.meal_id} @{self.url}"

class Cart(models.Model):
  user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
  total = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
  count = models.IntegerField(default=0, blank=True)
  active = models.BooleanField(default=True)

class Entry(models.Model):
  meal = models.ForeignKey(Meal, null=True, on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
  active = models.BooleanField(default=True)

@receiver(post_save, sender=Entry)
def update_cart(sender, instance, **kwargs):
  line_cost = instance.quantity * instance.meal.price
  instance.cart.total += line_cost
  instance.cart.count += instance.quantity
  instance.cart.save()

@receiver(pre_delete, sender=Entry)
def remove_cart(sender, instance, **kwargs):
  line_cost = instance.quantity * instance.meal.price
  instance.cart.total -= line_cost
  instance.cart.count -= instance.quantity
  instance.cart.save()

class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  comment = models.CharField(max_length=250)
  rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True)

class Transaction(models.Model):
  quantity = models.IntegerField(null=True)
  date = models.DateField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  total = models.DecimalField(null=True, default=0.00, max_digits=7, decimal_places=2)

# Create your models here.
