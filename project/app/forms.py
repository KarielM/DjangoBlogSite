from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class Create_User_Form(UserCreationForm):
    is_youTuber = forms.BooleanField(label = 'Are you a YouTuber?', required=False)
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
                role, created = Role.objects.get_or_create(name = 'Admin')
            else:
                role, created = Role.objects.get_or_create(name = 'Regular')

            UserProfile.objects.create(user=user, role=role)

        return user
    

class Create_Blog_Post_Form(forms.ModelForm):
    title = forms.CharField(required=True)
    
    class Meta:
        model = Posts
        fields = ['title', 'content_creator', 'post']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Create_Blog_Post_Form, self).__init__(*args, **kwargs)
        
            
        if user:
            youtubers_objects = YouTuber.objects.filter(subscription__subscriber=user)
            youtubers = User.objects.filter(pk__in=[i.creator.pk for i in youtubers_objects])
            # subscriptions = Subscription.objects.filter(subscriber=user)
            # youtubers_objects = YouTuber.objects.filter(subscription__subscriber=user)
            # print(youtubers)
            # print(subscriptions)
            # print (f' Youtubers: {youtubers}')
            self.fields['content_creator'].queryset = youtubers

class Update_Blog_Post_Form(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content_creator', 'post']