from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    objects = None
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    objects = None
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    objects = None
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-created'] # META - суперкласс, в данном случакпозволяющий сортировать по дате создания/обновления

    def __str__(self):
        return self.body[0:50] # сообщение будет содержать не более 50 символов на боковой панели
