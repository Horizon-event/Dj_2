from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'lets learn Python!!!'},
#     {'id': 2, 'name': 'lets learn C#!'},
#     {'id': 3, 'name': 'lets learn YAHOOO!'},
#     {'id': 4, 'name': 'lets learn Django!'}]


def loginPage(request):  # вход если зарегестрирован
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')  # если уже зарегистрирован, возвращение на главную страницу

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Пользователь не найден.')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):  # выход из регистрации
    logout(request)
    return redirect('home')


def registerPage(request):  # регистрация
    form = UserCreationForm()  # использование шаблона формы
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # бросаем данные пользователя в форму
        if form.is_valid():  # проверка на правильность заполнения формы
            user = form.save(commit=False)  # commit=False запрет на внесение изменений
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')  # Во время регистрации произошла ошибка

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # фильтруются сообщения по темам, если нет конкретной темы, выводится все
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    # фильтруются сообщения по темам комнаты.
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'Base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()  # .order_by('-created')сортировка по убыванию
    participants = room.participants.all()
    if request.method == 'POST':
        messages = Message.objects.create(
            users=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants} # для получения доступа внутри комнаты через словарь
    return render(request, 'Base/room.html', context)


@login_required(login_url='login') # декоратор не дает создать комнату без регистрации
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # вcе комнаты (темы, посты), созданные пользователем
    room_messages = user.message_set.all() # вcе комментарии, созданные пользователем
    # была проблема с отображением комментариев из за окончания s, т.к. в activity_component.html не room_message а
    # room_messages
    topics = Topic.objects.all() # список всех тем обсуждения
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login') # декоратор не дает обновить комнату без регистрации
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.users:
        return HttpResponse('Your are not allowed here!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})