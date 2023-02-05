from django.forms import ModelForm
from django import forms
from .models import Channel, Group, Filter
import datetime

class AddChannel(ModelForm):
  channel_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "smaller"}), label='Channel name')
  channel_group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select(attrs={'class': "smaller mb-1"}), label='Channel group')
  class Meta:
    model = Channel
    fields = ['channel_name', 'channel_group']

class CreateFilter(ModelForm):
  text_filter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Text filter', "class": "smaller mb-2"}), label='', required=False)
  translation_filter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Translation filter', "class": "smaller mb-2"}), label='', required=False)
  view_count = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "smaller"}), label='View count above', required=False)
  share_count = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "smaller mb-2"}), label='Share count above', required=False)
  start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "smaller"}), required=False)
  end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "smaller"}), required=False)
  class Meta:
    model = Filter
    fields = ['text_filter', 'translation_filter', 'view_count', 'share_count', 'start_date', 'end_date']