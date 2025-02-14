from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('message/<int:inbox_id>/', views.message_detail, name='message_detail'),
    path('send/', views.send_message, name='send_message'),
    path('archive/<int:inbox_id>/', views.archive_inbox, name='archive_inbox'),
]
