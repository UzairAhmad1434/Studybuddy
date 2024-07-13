from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:room_id>', views.room_view, name='room'),
    path('create_room/', views.create_room, name='createRoom'),
]

