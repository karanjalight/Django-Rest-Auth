from .views import *
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    #logging in and out
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('example/', ExampleView.as_view(), name='userdata-list'),
    
    
    path('userdata/', UserDataList.as_view(), name='userdata-list'),
    path('userdata/<int:pk>/', UserDataDetail.as_view(), name='userdata-detail'),
]