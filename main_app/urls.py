from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('profile/', views.profile, name='profile'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup', views.signup, name='signup'),
  path('meals/', views.index, name='index'),
  path('meals/create/', views.MealCreate.as_view(), name='meal_create'),
  path('meals/<int:meal_id>/', views.meal_detail, name='details'),
  path('meals/<int:pk>/update/', views.MealUpdate.as_view(), name='meal_update'),
  path('meals/<int:pk>/delete/', views.MealDelete.as_view(), name='meal_delete'),
  path('meals/<int:meal_id>/add_photo/', views.add_photo, name='add_photo'),
  path('cart/', views.my_cart, name='cart'),
  path('cart/<int:meal_id>/add_cart/<int:cart_id>/', views.add_cart, name='add_cart'),
  path('cart/<int:meal_id>/rmv_cart/<int:cart_id>/', views.rmv_cart, name='rmv_cart'),
]