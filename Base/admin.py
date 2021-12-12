from django.contrib import admin
from .models import Room, Topic, Message

# Register your models here.

admin.site.register(Room) # подключение шаблона Room к панели администратора
admin.site.register(Topic)
admin.site.register(Message)