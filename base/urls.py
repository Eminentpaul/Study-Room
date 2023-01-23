from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('topics/all', views.allTopics, name='topics'),
    path('room/create/', views.createRoom, name='create-room'),
    path('room/<str:pk>/roomEnvironment', views.rooms, name='room'),
    path('updateroom/<str:pk>/Update', views.updateRoom, name='updateroom'),
    path('deleteroom/<str:pk>/Delete', views.deleteRoom, name='deleteroom'),
    path('profile/<str:pk>/userProfile', views.profile, name='profile'),
    path('edit/editProfile', views.editUser, name='editprofile'),
    path('messages/deletechat/<str:pk>', views.deleteChat, name='deleteChat'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)