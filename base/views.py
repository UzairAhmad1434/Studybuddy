from django.shortcuts import render, get_object_or_404, redirect
from .models import Room
from .forms import RoomForm

def home(request):
     rooms = Room.objects.all()
     return render(request, 'base/home.html',{'rooms': rooms})

def room_view(request, room_id):
    rooms = get_object_or_404(Room, id=room_id)
    return render(request, 'base/room.html', {'room': rooms})

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        form = RoomForm()
    return render(request, 'base/room_form.html', {'form': form})

def update_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)  
        if form.is_valid():
            form.save()
            return redirect('room', room_id=room.id)
    else:
        form = RoomForm(instance=room)  
    return render(request, 'base/room_form.html', {'form': form})
