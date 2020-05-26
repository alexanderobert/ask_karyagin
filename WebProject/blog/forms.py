from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from taggit.forms import TagField

from .models import Question, Answer, Profile

class AddPost(forms.ModelForm):
  title = forms.CharField(label='Question title', widget=forms.TextInput(
          attrs={'class': 'form-control', 'maxlength': '70'}))
  text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'maxlength': '600'}),label='Question text')
  tags = TagField(label='Tags', widget=forms.TextInput(attrs={'class': 'form-control'}))
  class Meta:
    model = Question
    fields = ['title', 'text', 'tags']

  def __init__(self, author, *args, **kwargs):
    self.author = author
    super().__init__(*args, **kwargs)

  def save(self, commit=True):
    question = Question(**self.cleaned_data)
    question.author_id = self.author
    question.pub_date = timezone.now()
    if commit:
      question.save()
    return question

class AddAnswer(forms.ModelForm):
  class Meta:
    model = Answer
    fields = ['text']
    widgets = {
      'text': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '300', 'required': True, }),}

  def __init__(self, author, question, *args, **kwargs):
    self.author = author
    self.question = question
    super().__init__(*args, **kwargs)

  def save(self, commit=True):
    answer = Answer(**self.cleaned_data)
    answer.author_id = self.author
    answer.question = self.question

    answer.pub_date = timezone.now()
    if commit:
      answer.save()
    return answer

class UserRegistration(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['username', 'email', 'first_name', 'password', 'img',]
    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control','maxlength': '20', 'required': True,}),
      'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
      'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50',}),
      'password': forms.PasswordInput(),
    }

  def save(self, commit=True):
    profile = Profile(**self.cleaned_data)
    profile = super(UserRegistration, self).save()
    profile.is_active = True
    profile.set_password(profile.password)
    if commit:
      profile.save()
    return profile

    # def __init__(self, *args, **kwargs):
    #   super().__init__(*args, **kwargs)
    #
    # def save(self, commit=True):
    #   acc = User(**self.)
    #   acc.is_active = True
    #   acc.set_password(acc.password)
    #
    #   if commit:
    #     acc.save()
    #   return acc

class UserSetting(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['email', 'first_name', 'img', ]
    widgets = {
      'email': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
      'first_name': forms.TextInput(attrs={'class': 'form-control', }),
    }

  def __init__(self, profile, *args, **kwargs):
    self.profile = profile
    super().__init__(*args, **kwargs)

  def save(self, commit=True):
    profile = self.profile
    profile.email = self.data.get("email")
    profile.first_name = self.data.get("first_name")
    profile.img = self.files.get("img", default=profile.img)
    if commit:
      profile.save()
    return profile
