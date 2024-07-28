from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Message,User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import RoomForm,UserForm



def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get("username").lower()
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

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'something went wrong please try again')
        
    return render(request,'base/login_register.html',{'form':form})

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
    topics=Topic.objects.all()[0:4]
    room_count=rooms.count()
    room_message=Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'base/home.html',{'rooms': rooms,'topics':topics,'room_count':room_count,'room_message':room_message})

def profile(request,room_id):
    user=User.objects.get(id=room_id)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    return render(request,'base/profile.html',{'user':user,'rooms':rooms,'room_message':room_message,'topics':topics})

def room_view(request, room_id):
    room_instance = get_object_or_404(Room, id=room_id)
    messages = room_instance.message_set.all().order_by('-created')
    participants=room_instance.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room_instance,
            body=request.POST.get('body')
        )
        room_instance.participants.add(request.user)
        return redirect('room', room_id=room_instance.id)

    return render(request, 'base/room.html', {'room': room_instance, 'messages': messages,'participants':participants})

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    return render(request, 'base/room_form.html', {'form': form, 'topics': topics})

@login_required(login_url='/login')
def update_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    form=RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get("name")
        room.topic=topic
        room.description=request.POST.get("description")
        room.save()
        return redirect('room', room_id=room.id)
    
    if request.user!=room.host:
        return HttpResponse('you are not allowed here')
    return render(request, 'base/room_form.html', {'form': form,'room':room,'topics':topics})

@login_required(login_url='/login')
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user!=room.host:
        return HttpResponse('you are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'obj': room})

@login_required(login_url='/login')
def delete_message(request, room_id):
    message = get_object_or_404(Message, id=room_id)
    if request.user!=message.user:
        return HttpResponse('you are not allowed here')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'obj': message})

@login_required(login_url='/login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', room_id=user.id) 
    return render(request, 'base/update_profile.html', {'form': form})

def topicPage(request):
     topic=Topic.objects.filter()
     return render(request, 'base/topic.html', {'topic':topic})

def activityPage(request):
     message=Message.objects.all()
     return render(request, 'base/activity.html', {'message':message})