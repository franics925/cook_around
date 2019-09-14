from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
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
def home(request):
    return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignUpForm()
  profile_form = ProfileForm()
  context = {'form': form, 'error_message': error_message, 'profile_form': profile_form}
  return render(request, 'registration/signup.html', context)

def index(request):
  meals = Meal.objects.all()
  return render(request, 'wechef/index.html', { 'meals': meals })

def meals_detail(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  return render(request, 'meals/detail.html'), {
    'meal': meal
  }

class MealCreate(LoginRequiredMixin, CreateView):
  model = Meal
  fields = ['name', 'description', 'quantity', 'price']
  # success_url = '/index/'
  def form_valid(self, form):
    form.instance.chef = self.request.user
    return super().form_valid(form)






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