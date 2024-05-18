from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class Create_User_Form(UserCreationForm):
    is_youTuber = forms.BooleanField(label = 'Are you a YouTuber?')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        is_youTuber = self.cleaned_data.get('is_youTuber', False)

        if commit:
            user.save()

            if is_youTuber:
                YouTuber.objects.create(creator=user)
                role, created = Role.objects.get_or_create('Admin')
            else:
                role, created = Role.objects.get_or_create('Regular')

            UserProfile.objects.create(user=user, role=role)

        return user
    

class Create_Blog_Post_Form(forms.ModelForm):
    title = forms.CharField(required = True)
    class Meta:
        model = Posts
        # fields = ['user', 'creator', 'post', 'tags']
        # fields = ['title', 'content_creator', 'post']
        fields = ['title','content_creator', 'post']


class Update_Blog_Post_Form(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'post']