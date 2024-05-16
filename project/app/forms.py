from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Posts

class Create_User_Form(UserCreationForm):
    is_youTuber = forms.BooleanField(label = 'Are you a YouTuber?')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit = False)
        user.is_youTuber = self.cleaned_data.get('is_youTuber', False)
        if commit:
            user.save()
        return user
    

class Create_Blog_Post_Form(forms.Form):
    class Meta:
        model = Posts
        fields = ['user', 'creator', 'post', 'tags']
