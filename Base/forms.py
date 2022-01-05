from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # 'host' - автоматически добавляет автора новой комнаты (темы), без нее - можно выбрать из списка юзеров
        # 'participants' - убирает имена участников обсуждения - без можно выбрать
        exclude = ['host', 'participants']

