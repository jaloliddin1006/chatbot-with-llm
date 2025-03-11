from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_answer/', views.get_answer, name='get_chat_answer'),
    path('clear-history/', views.clear_history, name='clear-chat-history'),

]
