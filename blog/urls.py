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
    path('users/connect/<operation>/<pk>', views.change_friends, name='change_friends'),
    path('invites/', views.invites, name="invites"),
    path('invites/<int:pk>/<int:team>/<int:user>/accept/', views.invite_accept, name="invite_accept"),
    path('invites/<int:pk>/decline/', views.invite_decline, name="invite_decline"),
    path('invites/<int:user>/<int:team>/send/', views.invite_send, name="invite_send"),
    path('applications/', views.applications, name="applications"),
    path('applications/<int:pk>/<int:team>/<int:applicant>/accept/', views.application_accept, name="application_accept"),
    path('applications/<int:pk>/<int:team>/<int:applicant>/reject/', views.application_reject, name="application_reject"),
    path('applications/<int:pk>/join/', views.application_join, name="application_join"),
    path('teams/', views.teams, name="teams"),
    path('teams/create', views.create_team, name="create_team"),
    path('teams/<int:pk>', views.team_detail, name="team_detail"),
]