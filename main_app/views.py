from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import Meal
from main_app.forms import SignUpForm, ProfileForm
from .models import Meal

import uuid
# import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'cookaround-jbc'

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

def meal_detail(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  return render(request, 'meals/detail.html', {
    'meal': meal
  })





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