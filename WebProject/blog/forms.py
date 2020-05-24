from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from taggit.forms import TagField

from .models import Question, Answer, Profile

class add_post(forms.ModelForm):
  class Meta:
    model = Question
    exclude = ['votes', 'pub_date', 'author_id']

  title = forms.CharField(label='Question title', widget=forms.TextInput(
          attrs={'class': 'form-control', 'maxlength': '70',
                 'oninvalid': "this.setCustomValidity('Помогите')"})
                        )
  text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'maxlength': '600'}),label='Question text')
  tags = TagField(label='Tags', widget=forms.TextInput(attrs={'class': 'form-control'}))
  required_css_class= "field"

class add_answer(forms.ModelForm):
  class Meta:
    model = Answer
    exclude = ['votes', 'question', 'author_id', 'pub_date']
  text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'maxlength': '300'}), label='Answer text')

class user_registration(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['username', 'email', 'first_name', 'password', 'img',]
    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control','maxlength': '20', 'required': True,}),
      'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
      'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50',}),
      'password': forms.PasswordInput(),
      'img': forms.FileInput(attrs={'upload_to': 'user_images', 'accept': 'image/*', 'required': False,})
    }

class user_setting(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['email', 'first_name', 'img', ]
    widgets = {
      'email': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
      'first_name': forms.TextInput(attrs={'class': 'form-control', }),
      'img': forms.FileInput(attrs={'upload_to': 'user_images', 'accept': 'image/*'})
    }