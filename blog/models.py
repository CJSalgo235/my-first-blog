from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()    
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     description = models.CharField(max_length=100, default='')
     city = models.CharField(max_length=50, default='')
     website = models.URLField(max_length=100, default='')
     phone = models.CharField(max_length=20)
     image = models.ImageField(upload_to='profile_image', blank=True)

     def __str__(self):
         return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_pofile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)

class Team(models.Model):
    name = models.CharField(max_length=50, default='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    members = models.ManyToManyField(User, related_name='members')

    def __str__(self):
        return self.name

class Invite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitee')
    invited_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter')
    accepted_invite = models.BooleanField(default=False)
    declined_invite = models.BooleanField(default=False)

    def __str__(self):
        return self.invited_to
    
    def approve(self):
        self.accepted_invite = True
        self.save()
    
    def decline(self):
        self.declined_invite = True
        self.save()

class Application(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant')
    accepted_applicant = models.BooleanField(default=False)
    rejected_applicant = models.BooleanField(default=False)
    
    def __str__(self):
        return self.team

    def approve(self):
        self.accepted_applicant = True
        self.save()

    def decline(self):
        self.rejected_applicant = True
        self.save()

class Friend(models.Model):
    users = models.ManyToManyField(User, related_name='friend_set')
    current_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(current_user, new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(current_user, new_friend)
    
    def __str__(self):
        return str(self.current_user) + "'s friends"

