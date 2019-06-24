from django import forms

from .models import Post, Comment, Team

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.forms import AuthenticationForm
#These are all Custom Forms

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Username',
        }
    ))
    email = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'true',
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'true',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'ConfirmPassword',
            'required': 'true',
        }
    ))

    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
        }
    ))

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        ) 
        #exclude = ()

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)