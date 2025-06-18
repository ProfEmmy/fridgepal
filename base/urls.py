from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutView, name='logout'),

    path('', views.home, name='home'),

    path('add-item/', views.addItemPage, name='addItemPage'),
    path('edit-item/<str:pk>/', views.editItem, name='editItem'),
    path('delete-item/<str:pk>/', views.deleteItem, name='deleteItem'),
    path('item-details/<str:pk>/', views.itemPage, name='itemPage'),

    path('add-group/', views.addGroup, name='addGroup'),
    path('groups-page/', views.groupsPage, name='groupsPage'),
    path('edit-group/<str:pk>/', views.editGroup, name='editGroup'),
    path('delete-group/<str:pk>/', views.deleteGroup, name='deleteGroup'),

    path('edit-account/<str:pk>/', views.editAccount, name='editAccount'),
    path('change-password/<str:pk>', views.changePassword, name='changePassword')
]