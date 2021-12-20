from django.conf.urls.static import static
from django.urls import path

from capstone import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('discover', views.discover, name='discover'),
    path('feed', views.feed, name='feed'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('profile/<int:user_id>/follow', views.follow, name='follow'),
    path('profile/<int:user_id>/unfollow', views.unfollow, name='unfollow'),
    path('activity/<int:activity_id>/edit', views.edit_activity, name='edit_activity'),
    path('activity/<int:activity_id>/delete', views.delete_activity, name='delete_activity'),
    path('activity/<int:activity_id>', views.view_activity, name='view_activity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
