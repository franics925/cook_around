from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from main_app.forms import SignUpForm, ProfileForm
from .models import Meal, Photo, Cart, Review, Entry

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
      print(form.errors)
      error_message = form.errors
  form = SignUpForm()
  profile_form = ProfileForm()
  context = {'form': form, 'error_message': error_message, 'profile_form': profile_form}
  return render(request, 'registration/signup.html', context)

def index(request):
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
  my_cart, created = Cart.objects.get_or_create(user=user)
  entries = Entry.objects.all()
  meals = Meal.objects.all()
  if request.POST:
    meal_id = request.POST.get('meal_id')
    meal = Meal.objects.get(id=meal_id)
    quantity = Decimal(request.POST.get('meal_quantity'))
    Entry.objects.create(cart=my_cart, meal=meal, quantity=quantity)
  return render(request, 'wechef/cart.html', {
    'my_cart': my_cart,
    'user': user,
    'entries': entries,
  })

def add_cart(request, cart_id, meal_id):
  Cart.objects.get(id=cart_id).meals.add(meal_id)
  return redirect('details', meal_id=meal_id)

def rmv_cart(request, cart_id, meal_id):
  Cart.objects.get(id=cart_id).meals.remove(meal_id)
  return redirect('cart')


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