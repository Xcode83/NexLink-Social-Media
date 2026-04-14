from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='social/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='social/logout.html'), name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('explore/', views.explore, name='explore'),
    path('search/', views.search_users, name='search_users'),
    path('friend-request/send/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('friend-request/accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.post_comment, name='post_comment'),
]
