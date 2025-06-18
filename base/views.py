from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib import messages
from .models import Item, Group
from .form import ItemForm, GroupForm, UserEditForm

# Create your views here.
def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if form.is_valid:
            username_exists = User.objects.filter(username=username).exists()
            if username_exists:
                messages.error(request, 'username is taken')
                return redirect('registerPage')
            elif len(password) <= 8:
                messages.error(request, 'password should have minimum 8 characters')
            elif password.isalpha():
                messages.error(request, 'password must contain at least a number')
            elif ' ' in password:
                messages.error(request, "password shouldn't contain spaces")
            elif password.isdigit():
                messages.error(request, 'passoword must contain letters')
            else:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()

                login(request, user)

                messages.success(request, 'registered successfully')

                return redirect('home')

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'base/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'user not found')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is not correct')

    return render(request, 'base/login.html')

@login_required(login_url='/login')
def logoutView(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='/login')
def home(request):
    items = Item.objects.filter(user=request.user).order_by('-created')
    for index, item in enumerate(items):
        if index % 2 == 0:
            item.even = True
        else:
            item.even = False
    context = {'items': items, 'user': request.user }

    return render(request, 'base/home.html', context)

@login_required(login_url='/login')
def addItemPage(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        expiring_date = request.POST.get('expiring_date')
        recommended_groups = request.POST.get('recommended_groups')
        if form.is_valid:
            item = form.save(commit=False)
            item.user = request.user
            item.expiring_date = expiring_date
            item.recommended_groups = Group.objects.get(group_name=recommended_groups)
            item.save()

            messages.success(request, 'Item Added Successfully')
            return redirect('home')

    form = ItemForm()
    groups = Group.objects.filter(Q(user=request.user) | Q(user=None))

    context = {'form': form, 'groups':groups}
    return render(request, 'base/add_item.html', context)

@login_required(login_url='/login')
def editItem(request, pk):
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid:
            form.save(commit=False)
            form.save()

            messages.success(request, 'Item Updated')
            return redirect('home')


    context = {'form': form}
    return render(request, 'base/add_item.html', context)

@login_required(login_url='/login')
def deleteItem(request, pk):
    item = Item.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Deleted Successfuly')
        return redirect('home')

    context = {'item': item}
    return render(request, 'base/delete_item.html', context)

@login_required(login_url='/login')
def itemPage(request, pk):
    item = Item.objects.get(id=pk)

    context = {'item': item}
    return render(request, 'base/item.html', context)

def addGroup(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid:
            group_name = request.POST.get('group_name')
            group_exists = Group.objects.filter(group_name=group_name)
            if len(group_exists) != 0:
                messages.error(request, 'Group already created')
            else:
                group = form.save(commit=False)
                group.user = request.user
                group.save()
                messages.success(request, 'Group successfully created')

    form = GroupForm()

    context = {'form': form}
    return render(request, 'base/add_group.html', context)

def groupsPage(request):
    groups = Group.objects.filter(Q(user=request.user) | Q(user=None))

    context = {'groups': groups}
    return render(request, 'base/groups_page.html', context)

def editGroup(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid:
            form.save()
            return redirect('groupsPage')

    context = {'form':form}
    return render(request, 'base/add_group.html', context)

def deleteGroup(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('groupsPage')

    return render(request, 'base/delete.html')

def editAccount(request, pk):
    account = User.objects.get(id=pk)
    form = UserEditForm(instance=account)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=account)
        username = request.POST.get('username')
        if form.is_valid:
            username_exists = User.objects.filter(username=username).exists()
            if username_exists:
                messages.error(request, 'username is taken')
                return redirect('editAccount', account.id)
            else:
                form.save()
                messages.success(request, 'username edited successfully')
                return redirect('home')

    context = {'form': form}
    return render(request, 'base/edit-account.html', context)

def changePassword(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        username = user.username
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = authenticate(username=username, password=old_password)
        if user is not None:
            if new_password == confirm_password:
                if len(new_password) <= 8:
                    messages.error(request, 'password should have minimum 8 characters')
                elif new_password.isalpha():
                    messages.error(request, 'password must contain at least a number')
                elif ' ' in new_password:
                    messages.error(request, "password shouldn't contain spaces")
                elif new_password.isdigit():
                    messages.error(request, 'passoword must contain letters')
                
                else:
                    user_ = User.objects.get(id=pk)
                    user_.set_password(new_password)
                    user_.save()

                    messages.success(request, 'password changed successfully')
                    return redirect('home')

            else:
                messages.error(request, "passords don't match")
        else:
            messages.error(request, 'password is not correct')

    return render(request, 'base/change-password.html')