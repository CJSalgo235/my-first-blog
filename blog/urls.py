from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import (
        password_reset, 
        password_reset_done,
        password_reset_confirm,
    )

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.view_profile, name='profile'),
    path('accounts/profile/edit', views.edit_profile, name='edit_profile'),
    path('accounts/change-password', views.change_password, name='change_password'),
    path('accounts/reset-password', password_reset, name='reset_password'),
    path('accounts/reset-password/done', password_reset_done, name='password_reset_done'),
    path('users', views.users, name="users"),
    path('users/connect/<operation>/<pk>', views.change_friends, name='change_friends')
]