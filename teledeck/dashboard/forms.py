from django.forms import ModelForm
from django import forms
from .models import Channel, Group

class AddChannel(ModelForm):
  channel_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': "mb-3"}), label='Channel name')
  channel_group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Channel group')
  class Meta:
    model = Channel
    fields = ['channel_name', 'channel_group']