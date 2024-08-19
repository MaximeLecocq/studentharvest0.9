from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    # path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/start/<int:listing_pk>/', views.start_conversation, name='start_conversation'),

    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),

]


    # path('start-conversation/<int:listing_id>/', views.start_conversation, name='start_conversation'),
