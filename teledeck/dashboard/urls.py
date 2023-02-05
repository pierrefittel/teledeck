from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-channel', views.add_channel, name='add-channel'),
    path('create-filter', views.create_filter, name='create-filter'),
    path('toggle-channel/<channel_name>', views.toggle_channel, name='toggle-channel'),
    path('toggle-group/<channel_group>', views.toggle_group, name='toggle-group'),
    path('delete-channel/<channel_name>', views.delete_channel, name='delete-channel'),
    path('show-detail/<id>', views.show_detail, name='show-detail'),
]