from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('', views.home, name='home'),
    path('room/<int:room_id>', views.room_view, name='room'),
    path('create_room/', views.create_room, name='createRoom'),
    path('update_room/<int:room_id>', views.update_room, name='updateRoom'),
    path('delete_room/<int:room_id>', views.delete_room, name='deleteRoom'),
]

