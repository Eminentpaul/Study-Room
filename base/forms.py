from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Topic, Room, Message, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['image', 'name', 'username', 'email', 'bio']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['created', 'updated', 'host', 'participant']