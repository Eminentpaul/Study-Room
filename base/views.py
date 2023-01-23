from django.shortcuts import render, redirect
from .models import User, Room, Topic, Message
from django.contrib.auth.models import auth
from django.contrib import messages as mg
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, RoomForm, UserForm


# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else: mg.info(request, 'Invalid Username or Password')

    return render(request, 'login.html')

def signup(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        forms = MyUserCreationForm(request.POST, request.FILE)
        if forms.is_valid():
            # print('donecx')
            user = forms.save()
            auth.login(request, user)
            return redirect('home')
        else: mg.info(request, 'Registration is not Successful')
    return render(request, 'signup.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:3]

    messages = Message.objects.all()

    context = {'rooms': rooms, 'topics': topics, 'messages': messages}
    return render(request, 'index.html', context)

def settings(request):
    return render(request, 'settings.html')

def editUser(request):
    profile = request.user
    form = UserForm(instance=profile)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=profile.id)

    context = {'form':form}
    return render(request, 'edit-user.html', context)

def allTopics(request):
    topics = Topic.objects.all()
    return render(request, 'topics.html', {'topics': topics})

@login_required(login_url='login')
def rooms(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    if request.method == 'POST':
        conversation  = Message.objects.create(
            user = request.user,
            name = room,
            body = request.POST['message']
        )
        conversation.save()
        room.participant.add(request.user)
        return redirect('room', pk=room.id)

    participants = room.participant.all()

    context = {'room':room, 'messages':messages, 'participants': participants}
    return render(request, 'room.html', context)


def profile(request, pk):
    profile = User.objects.get(id=pk)
    rooms = profile.room_set.all()
    messages = profile.message_set.all()
    topics = Topic.objects.all()
    context = {'profile': profile, 'rooms': rooms, 'messages':messages, 'topics': topics}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    room_form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST['name'],
            description = request.POST['description']
        )

        return redirect('home')
    return render(request, 'create-room.html', {'room_form': room_form, 'topics': topics })

def updateRoom(request, pk):
    update = True
    room = Room.objects.get(id=pk)
    room_form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST['name']
        room.topic.name = topic,
        room.description = request.POST['description']
        room.save()
        return redirect('home')
    context = {'room_form': room_form, 'room':room, 'topics': topics, 'update': update}
    return render(request, 'create-room.html', context)

def deleteChat(request, pk):
    obj = Message.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    context = {'obj':obj}
    return render(request, 'delete.html', context)

def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    context = {'obj':obj}
    return render(request, 'delete.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')