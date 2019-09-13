from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField
  chef = models.BooleanField()
  address1 = models.CharField(max_length=50)
  address2 = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=30)
  zipcode = models.IntegerField()

class Meal(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=50)
  quantity = models.IntegerField()
  price = models.IntegerField()
  chef = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('details', kwargs={'meal_id': self.id})

class Transaction(models.Model):
  quantity = models.IntegerField()
  date = models.DateField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

class Photo(models.Model):
  url = models.CharField(max_length=200)
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for meal_id: {self.meal_id} @{self.url}"

# Create your models here.