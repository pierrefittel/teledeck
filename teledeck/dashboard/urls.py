from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update-data', views.update_data, name='update-data'),
    path('add-channel', views.add_channel, name='add-channel'),
    path('delete-channel/<channel_name>', views.delete_channel, name='delete-channel'),
    path('create-filter', views.create_filter, name='create-filter'),
    path('toggle-filter/<filter_id>', views.toggle_filter, name='toggle-filter'),
    path('delete-filter/<filter_id>', views.delete_filter, name='delete-filter'),
    path('toggle-channel/<channel_name>', views.toggle_channel, name='toggle-channel'),
    path('toggle-group/<channel_group>', views.toggle_group, name='toggle-group'),
    path('update-messages', views.filter_messages, name='update-messages'),
    path('csv-export', views.export_CSV, name='csv-export'),
]