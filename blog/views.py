from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, RegistrationForm, EditProfileForm, CreateTeamForm
from .models import Post, Comment, Friend, Team, Invite, Application
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.

def post_list(request): 
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    teams = Team.objects.filter(posted_to=post)

    args = {
        'post': post,
        'teams': teams
    }
    return render(request, 'blog/post_detail.html', args)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_new_to_team(request, team):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()          
            post = get_object_or_404(Post, pk=post.pk)
            post.team.add(team) 
            post.save()
            return redirect('team_detail', pk=team)
            
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def posts(request):
    private_posts = Post.objects.filter(published_date__isnull=True).order_by('created_date').filter(author=request.user.pk)
    public_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(author=request.user.pk) 

    args = {
        'private_posts': private_posts,
        'public_posts': public_posts,
        "posts_page": "active",
    }

    return render(request, 'blog/posts.html', args)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
 
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = RegistrationForm()

            args = {'form': form}
            return render(request, 'registration/register.html', args)

@login_required
def view_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    private_posts = Post.objects.filter(published_date__isnull=True).order_by('created_date').filter(author=request.user.pk)
    public_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(author=pk)

    args = {
        'user': user,
        'private_posts': private_posts,
        'public_posts': public_posts,
    }

    return render(request, 'blog/profile.html', args)

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'blog/edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        
        else:
            return redirect('/accounts/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'blog/change_password.html', args)

@login_required
def users(request):
    users = User.objects.exclude(id=request.user.id)
    friends = Friend.objects.get(current_user=request.user)
    friends = friends.users.exclude(id=request.user.id)

    args = {'users': users, 'friends': friends}
    return render(request, 'blog/users.html', args)

@login_required
def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('/users')

@login_required
def invites(request):
    team = Team.objects.filter(creator=request.user)
    invites = Invite.objects.exclude(
        invited_to__in=team,
        invited_by=request.user
    )
    
    args = {
        'invites': invites,
        "invites_page": "active"
    }
    return render(request, 'blog/invites.html', args)

@login_required
def invite_accept(request, pk, team, user):
    invite = get_object_or_404(Invite, pk=pk)
    invite.accept()
    invite.save()
    team = get_object_or_404(Team, pk=team)
    team.members.add(user)
    team.save() 
    return redirect('invites')

@login_required
def invite_decline(request, pk,):
    invite = get_object_or_404(Invite, pk=pk)
    invite.decline()
    invite.save()
    return redirect('invites')

@login_required
def invite_send(request, user, team):
    invite = Invite(invited_by=request.user)
    invite.invited_to = get_object_or_404(Team, pk=team)
    invite.user = get_object_or_404(User, pk=user)
    invite.save()
    return redirect('/teams/'+str(team))

@login_required
def applications(request):
    #teams = Team.objects.filter(creator=request.user) 
    applications = Application.objects.filter(team__creator__username=request.user)
    
    args = {
        'applications': applications,
        "applications_page": "active"
    }
    return render(request, 'blog/applications.html', args)

@login_required
def application_accept(request, pk, team, applicant):
        application = get_object_or_404(Application, pk=pk)
        application.approve()
        application.save()
        team = get_object_or_404(Team, pk=team)
        team.members.add(applicant)
        team.save()
        return redirect('/applications')

@login_required
def application_reject(request, pk, team):
    application = get_object_or_404(Application, pk=pk)
    application.reject()
    return redirect('applications')

@login_required
def application_join(request, pk):
    application = Application(applicant=request.user)
    application.team = get_object_or_404(Team, pk=pk)
    application.save()  
    team = get_object_or_404(Team, pk=pk)
    return redirect('teams')

@login_required
def teams(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()
            team = get_object_or_404(Team, pk=team.pk)
            team.members.add(request.user)
            return redirect('/teams')
    else: 
        all_teams = Team.objects.all()
        created_teams = Team.objects.filter(creator=request.user)
        joined_teams = Team.objects.filter(members__username=request.user).filter(~Q(creator=request.user))
        other_teams = Team.objects.filter(~Q(members__username=request.user))
        applications = Application.objects.filter(applicant=request.user)
        sent_applications = Team.objects.filter(team_application__in=Application.objects.filter(applicant=request.user))
        #sent_applications = Team.objects.filter(sent_applications=request.user)
        #other_teams_applications = zip(other_teams, applications)
        user = User.objects.get(id=request.user.id)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        form = CreateTeamForm() #Create Team Form

        args = {
            'all_teams': all_teams,
            'created_teams': created_teams,
            'joined_teams': joined_teams,
            'other_teams': other_teams,
            'applications': applications,
            'sent_applications': sent_applications,
            #'other_teams_applicatins': other_teams_applications,
            'user': user,
            'posts': posts,
            "teams_page": "active",
            'form': form
            
        }
        return render(request, 'blog/teams.html', args)

@login_required
def create_team(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()
            team = get_object_or_404(Team, pk=team.pk)
            team.members.add(request.user)
            return redirect('/teams')
    else:
        form = CreateTeamForm()
    return render(request, 'blog/create_team.html', {'form': form})

@login_required
def team_detail(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()          
            post = get_object_or_404(Post, pk=post.pk)
            post.team.add(team) 
            post.save()
            return redirect('team_detail', pk=team)
    else:
        team = get_object_or_404(Team, pk=pk)
        team_members = User.objects.filter(members=team)
        non_members = User.objects.filter(~Q(members=team))
        private_posts = Post.objects.filter(team=pk)
        public_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(team=pk)
        sent_invites = User.objects.filter(invitee__in=Invite.objects.filter(invited_to=team))
        form = PostForm()

        args = {
            'team': team,
            'team_members': team_members,
            'non_members': non_members,
            'private_posts': private_posts,
            'public_posts': public_posts,
            'sent_invites': sent_invites,
            'form': form
        }
        return render(request, 'blog/team_details.html', args)