from django.contrib import admin
from .models import Post, Comment, UserProfile, Team, Invite, Application, Friend

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(Application)
admin.site.register(Friend)