from django.forms import ModelForm
from django import forms
from .models import Channel, Group, Filter
import datetime

class AddChannel(ModelForm):
  channel_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "mb-2"}), label='Channel name')
  channel_group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Channel group')
  class Meta:
    model = Channel
    fields = ['channel_name', 'channel_group']

class CreateFilter(ModelForm):
  text_filter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Text filter', "class": "mb-3"}), label='')
  translation_filter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Translation filter', "class": "mb-3"}), label='')
  view_count = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "mb-3"}))
  share_count = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "mb-3"}))
  start_date = forms.DateField(initial=datetime.date.today)
  end_date = forms.DateField(initial=datetime.date.today)
  class Meta:
    model = Filter
    fields = ['text_filter', 'translation_filter', 'view_count', 'share_count', 'start_date', 'end_date']