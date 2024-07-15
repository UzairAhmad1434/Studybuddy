from django.shortcuts import render, get_object_or_404, redirect
from .models import Room,Topic
from django.db.models import Q
from .forms import RoomForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    if q:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    else:
        rooms = Room.objects.all()
    topics=Topic.objects.all()
    return render(request, 'base/home.html',{'rooms': rooms,'topics':topics})

def room_view(request, room_id):
    rooms = get_object_or_404(Room, id=room_id)
    return render(request, 'base/room.html', {'room': rooms})

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm()  # Initialize the form for GET requests

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

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'obj': room})