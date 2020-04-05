from django import forms
from taggit.forms import TagField

from .models import Question

class add_post(forms.ModelForm):
  class Meta:
    model = Question
    exclude = ['votes', 'pub_date', 'author_id']

  title = forms.CharField(label='Question title', widget=forms.TextInput(attrs={'class': 'form-control'}))
  text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),label='Question text')
  tags = TagField(label='Tags', widget=forms.TextInput(attrs={'class': 'form-control'}))
  required_css_class= "field"