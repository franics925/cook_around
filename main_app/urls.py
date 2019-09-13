from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup', views.signup, name='signup'),
  path('wechef/', views.index, name='index'),
  path('meals/create/', views.MealCreate.as_view(), name='create_meal'),
  path('meals/<int:meal_id/', views.meals_detail, name='detail'),
]