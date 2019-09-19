from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Entry, Review
from bootstrap_modal_forms.forms import BSModalForm

class SignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('chef', 'address1', 'address2', 'city', 'state', 'zipcode')

class ReviewForm(BSModalForm):
  class Meta:
    model = Review
    fields = ['rating', 'comment']


