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
  path('meals/<int:meal_id>/add_review/', views.add_review, name='add_review'),
  path('cart/', views.my_cart, name='cart'),
  path('cart/<int:pk>/rmv_entry/', views.EntryDelete.as_view(), name='rmv_entry'),
  path('cart/<int:pk>/clr_cart/', views.CartDelete.as_view(), name='clr_cart'),
  path('cart/<int:cart_id>/create_tran/', views.create_tran, name='create_tran'),
]