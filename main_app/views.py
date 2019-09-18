from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from main_app.forms import SignUpForm, ProfileForm
from .models import Meal, Photo, Cart, Review, Entry, Transaction

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'wechef'

# Create your views here.
class MealCreate(LoginRequiredMixin, CreateView):
  model = Meal
  fields = ['name', 'description', 'quantity', 'price']
  def form_valid(self, form):
    form.instance.chef = self.request.user
    return super().form_valid(form)

class MealDelete(LoginRequiredMixin, DeleteView):
  model = Meal
  success_url = '/meals/'

class MealUpdate(LoginRequiredMixin, UpdateView):
  model = Meal
  fields = ['name', 'description', 'quantity', 'price']

class CartDelete(LoginRequiredMixin, DeleteView):
  model = Cart
  def get_success_url(self):
        return reverse_lazy('cart')

class EntryDelete(LoginRequiredMixin, DeleteView):
  model = Entry
  def get_success_url(self):
        return reverse_lazy('cart')

def home(request):
    return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      profile_form = ProfileForm(request.POST, instance=user.profile)
      profile_form.full_clean()
      profile_form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = form.errors
  form = SignUpForm()
  profile_form = ProfileForm()
  context = {'form': form, 'error_message': error_message, 'profile_form': profile_form}
  return render(request, 'registration/signup.html', context)

def index(request):
  user = request.user
  filt = {'user': user, 'active': True}
  # my_cart, created = Cart.objects.get_or_create(user=user, active=True)
  my_cart = Cart.objects.filter(**filt).first()
  if not my_cart:
    my_cart = Cart.objects.create(user=user)
  meals = Meal.objects.all()
  return render(request, 'meals/index.html', { 'meals': meals })

def profile(request):
  user = request.user
  return render(request, 'wechef/profile.html', {'user': user})

def meal_detail(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  return render(request, 'meals/detail.html', {
    'meal': meal
  })

def add_photo(request, meal_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, meal_id=meal_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('details', meal_id=meal_id)

def my_cart(request):
  user = request.user
  filt = {'user': user, 'active': True}
  # my_cart, created = Cart.objects.get_or_create(user=user, active=True)
  my_cart = Cart.objects.filter(**filt).first()
  efilt = {'cart': my_cart, 'active': True}
  print(my_cart)
  if not my_cart:
    my_cart = Cart.objects.create(user=user)
  entries = Entry.objects.filter(**efilt)
  if request.POST:
    meal_id = request.POST.get('meal_id')
    meal = Meal.objects.get(id=meal_id)
    quantity = Decimal(request.POST.get('meal_quantity'))
    price = meal.price
    if (quantity <= meal.quantity):
      Entry.objects.create(cart=my_cart, meal=meal, quantity=quantity, price=price)
  return render(request, 'wechef/cart.html', {
    'my_cart': my_cart,
    'user': user,
    'entries': entries,
  })

def create_tran(request, cart_id):
  user = request.user
  filt = {'user': user, 'active': True}
  my_cart = Cart.objects.filter(**filt).first()
  entries = Entry.objects.filter(cart=my_cart)
  for entry in entries:
    entry.active = False
    entry.save()
  tran = Transaction.objects.create(user=user, cart=my_cart)
  my_cart.active = False
  my_cart.save()
  return render(request, 'wechef/transaction.html', {
    'my_cart': my_cart,
    'user': user,
    'entries': entries,
    'tran': tran
  })

def add_review(request, meal_id):
  form = ReviewForm(request.POST)
  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.meal_id = meal_id
    new_review.user = request.user
    new_review.save()
  return redirect('details', meal_id=meal_id)


# class BlogSearchListView(BlogListView):
#     """
#     Display a Blog List page filtered by the search query.
#     """
#     paginate_by = 10

#     def get_queryset(self):
#         result = super(BlogSearchListView, self).get_queryset()

#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(content__icontains=q) for q in query_list))
#             )

# return result