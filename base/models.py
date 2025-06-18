from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
def get_default_user():
    return User.objects.get(username='user')

class Classification(models.Model):
    class_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name
    
class UsersGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    group_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

class Group(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

class Item(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True)
    recommended_groups = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    # other_groups = models.ForeignKey(UsersGroup, on_delete=models.CASCADE, null=True, blank=True)
    expiring_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-created']

    def __str__(self):
        return self.name