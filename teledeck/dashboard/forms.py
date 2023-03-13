from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import Channel, Group, Filter, Parameter

class AddChannel(ModelForm):
  channel_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "smaller"}), label='Channel name')
  channel_group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select(attrs={'class': "smaller mb-1"}), label='Channel group')
  class Meta:
    model = Channel
    fields = ['channel_id', 'channel_name', 'channel_title', 'channel_group']

class CreateFilter(ModelForm):
  filter_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Filter name', "class": "smaller mb-2"}), label='', required=False)
  text_filter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Text filter', "class": "smaller mb-2"}), label='', required=False)
  translation_filter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Translation filter', "class": "smaller mb-2"}), label='', required=False)
  view_count = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "smaller"}), label='View count above', required=False)
  share_count = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "smaller mb-2"}), label='Share count above', required=False)
  start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "smaller"}), required=False)
  end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "smaller"}), required=False)
  class Meta:
    model = Filter
    fields = ['filter_name', 'text_filter', 'translation_filter', 'view_count', 'share_count', 'start_date', 'end_date']

class UserLogin(ModelForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "smaller"}), label='Username')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': "smaller"}), label='Password')
  class Meta:
    model = User
    fields = ['username', 'password']

class UserParameters(ModelForm):
  user_picture = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "smaller"}), label='User picture path')
  user_phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "smaller"}), label='User phone number')
  message_retrieve_limit = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "smaller"}), label='Message retrieve limit (in days)', required=True)
  api_id = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "smaller"}), label='API ID', required=True)
  api_hash = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "smaller"}), label='API hash')
  class Meta:
    model = Parameter
    fields = ['user_picture', 'user_phone', 'message_retrieve_limit', 'api_id', 'api_hash']