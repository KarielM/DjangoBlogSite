from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class YouTuber(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # subscribers = models.ManyToManyField(User, related_name='subscribed_to')

    def __str__(self):
        return self.creator.username

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='required')
    content_creator = models.ForeignKey(YouTuber, on_delete=models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# class Tag(models.Model):
#     name = models.CharField(max_length=25)
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete = models.CASCADE)
    subscribed_to = models.ForeignKey(YouTuber, on_delete = models.CASCADE)

# class Blocked_Subscriber(models.Model):
    #Fields: ID, blocker (foreign key to VTuber), blocked_user (foreign key to User), date_blocked, etc.
    # subscriber = models.ForeignKey(User, on_delete = models.CASCADE)
    # subscribed_to = models.ForeignKey(YouTuber, on_delete = models.CASCADE)


############################Creation Models########################
def create_YouTuber(name, subscribers):
    pass


def create_posts(author, title, creator, post):
    #dynamic input fields w/ plus mark
    #on submit collect all tags and pass them to create_posts as a list
    Posts.objects.create(author = author
                         ,title = title
                                ,content_creator = creator
                                ,post = post
                                )
    
def create_userprofile(user, role):
    UserProfile.objects.create(user=user, role=role)

def create_YouTuber(user, subscribers = None):
    user = YouTuber.objects.create(user=user)

    if subscribers:
        for subscriber in subscribers:
            user.subscribers.add(subscriber)

    return user

def create_role(role):
    return Role.objects.get_or_create(name = role)
# def create_Subscription(subscriber, creator):
#     return Subscription.objects.create(subscriber = subscriber
#                                 ,subscribed_to = creator)

# def create_Blocked_Subscriber(subscriber, creator):
#     return Blocked_Subscriber.objects.create(subscriber = subscriber
#                                              ,subscribed_to = creator)

############################Read Models########################
def view_all_posts(user):
    return Posts.objects.filter(author = user)

def view_role(user):
    try:
        user = UserProfile.objects.get(user = user)
        return user.role
    except:
        pass


############################Update Models########################
def update_certain_post(title, new_title, new_content, creator):
    try:
        post = Posts.objects.get(title=title
                                 , content_creator=creator)

        if new_title:
            post.title = new_title
        if new_content:
            post.post = new_content
        post.save()   
    except:
        pass
############################Delete Models########################
def delete_post(title, user):
    Posts.objects.get(title = title, author = user).delete()

############################Filter Models########################
def filter_by_title(title, user):
    Posts.objects.get(title =title, user = user)

def view_all_posts_associated(creator):
    return Posts.objects.filter(content_creator = creator)
        
