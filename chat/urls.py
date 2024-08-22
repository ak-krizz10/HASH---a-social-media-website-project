from django.urls import path
from chat import views
urlpatterns = [
    # path('inbox', views.inbox, name='inbox'),
    # path('chats/<username>', views.Chats, name='chats'),
    path('', views.dm, name='chats'),
    # path('send', views.SendMessage, name='send-message')
    path('link/<int:id>',views.newthread,name="link"),
]