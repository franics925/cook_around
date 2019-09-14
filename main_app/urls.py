from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup', views.signup, name='signup'),
  path('meals/', views.index, name='index'),
  path('meals/create/', views.MealCreate.as_view(), name='meal_create'),
  path('meals/<int:meal_id>/', views.meal_detail, name='details'),
  path('meals/<int:pk>/update/', views.MealUpdate.as_view(), name='meal_update'),
  path('meals/<int:pk>/delete/', views.MealDelete.as_view(), name='meal_delete'),
]