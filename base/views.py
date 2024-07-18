from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room,Topic
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import RoomForm



def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')

    context={}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')



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
    room_count=rooms.count()
    return render(request, 'base/home.html',{'rooms': rooms,'topics':topics,'room_count':room_count})



def room_view(request, room_id):
    rooms = get_object_or_404(Room, id=room_id)
    return render(request, 'base/room.html', {'room': rooms})

@login_required(login_url='/login')
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
    
    if request.user!=room.host:
        return HttpResponse('you are not allowed here')
    return render(request, 'base/room_form.html', {'form': form})

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user!=room.host:
        return HttpResponse('you are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'obj': room})