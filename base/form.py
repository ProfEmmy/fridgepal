from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Item, Group

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ['user', 'expiring_date', 'recommended_groups']

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['user']

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']