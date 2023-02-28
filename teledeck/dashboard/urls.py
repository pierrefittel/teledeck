from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.index, name='index'),
    path('check-api-auth', views.check_API_auth, name='check-api-auth'),
    path('update-data', views.update_data, name='update-data'),
    path('settings', views.settings, name='settings'),
    path('add-channel', views.add_channel, name='add-channel'),
    path('delete-channel/<channel_name>', views.delete_channel, name='delete-channel'),
    path('create-filter', views.create_filter, name='create-filter'),
    path('toggle-filter/<filter_id>', views.toggle_filter, name='toggle-filter'),
    path('delete-filter/<filter_id>', views.delete_filter, name='delete-filter'),
    path('toggle-channel/<channel_name>', views.toggle_channel, name='toggle-channel'),
    path('toggle-group/<channel_group>', views.toggle_group, name='toggle-group'),
    path('update-messages', views.filter_messages, name='update-messages'),
    path('sort-by-date', views.filter_messages, name='sort-by-date'),
    path('csv-export', views.export_CSV, name='csv-export'),
    path('get-message-detail/<message_id>', views.get_message_detail, name='get-message-detail'),
    path('get-data', views.get_data, name='get-data'),
    path('sign-out', views.sign_out, name='sign-out'),
]

urlpatterns += staticfiles_urlpatterns()