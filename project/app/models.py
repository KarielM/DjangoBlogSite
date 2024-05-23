from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

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
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title
    
# class Tag(models.Model):
#     name = models.CharField(max_length=25)
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete = models.CASCADE, related_name='subscriptions')
    subscribed_to = models.ForeignKey(YouTuber, on_delete = models.CASCADE)

    def __str__(self):
        return self.subscribed_to.creator.username


class Blocked_Subscriber(models.Model):
    subscriber = models.ForeignKey(User, on_delete = models.CASCADE)
    subscribed_to = models.ForeignKey(YouTuber, on_delete = models.CASCADE)


############################Creation Models########################

def create_posts(author, title, creator, post, created_at=None):
    created_at = datetime.now()

    existing_post = Posts.objects.filter(title=title, content_creator=creator).exists()
    if not existing_post:
        return Posts.objects.create(
            author=author,
            title=title,
            content_creator=creator,
            post=post,
            created_at=created_at
        )
        
    else:
        return "A post with the same title already exists."
    
def create_userprofile(user, role):
    UserProfile.objects.create(user=user, role=role)

def create_YouTuber(user, subscribers = None):
    return YouTuber.objects.create(user=user)


def create_blocked_user(user, subscribed_to):
    return Blocked_Subscriber.objects.get_or_create(subscriber = user
                                             , subscribed_to = subscribed_to)

def create_role(role):
    return Role.objects.get_or_create(name = role)

def create_Subscription(subscriber, creator):
    youTuber, created = Subscription.objects.get_or_create(subscriber = subscriber
                                ,subscribed_to = creator)
    
    return youTuber


############################Read Models########################
def view_all_posts(user):
    return Posts.objects.filter(author = user)

def view_role(user):
    try:
        user = UserProfile.objects.get(user = user)
        return user.role
    except:
        pass

def view_all_youTubers():
    return YouTuber.objects.all()

def view_latest_post(user, subscribed_to):
    try:
        list = Posts.objects.filter(author = user
                             ,content_creator = subscribed_to)
    except:
        pass

def view_single_blog_by_title(author, title, creator):
    try: 
        Posts.objects.get(author = author,
                          title = title,
                          content_creator = creator,
                          )
    except:
        pass

def view_single_blog_reverse_lookup(author, title, creator):
        return Posts.objects.get(author = author
                        ,title = title 
                        ,content_creator = creator)

def view_all_blocked(user):
    return Blocked_Subscriber.objects.filter(subscriber = user)

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

def delete_subscription(user, subscribed_to):
    Subscription.objects.get(subscriber = user, subscribed_to = subscribed_to).delete()

def delete_or_unblock_blocked_user(user, youtuber):
    Blocked_Subscriber.objects.get(subscriber = user, subscribed_to = youtuber).delete()
############################Filter Models########################
def filter_by_title(title, user):
    Posts.objects.get(title =title, user = user)

def view_all_posts_associated(creator):
    return Posts.objects.filter(content_creator = creator)
        
def filter_all_subscriptions(user):
    return Subscription.objects.filter(subscriber = user)

def find_all_subscribers(creator):
    try:
        creator = YouTuber.objects.get(creator = creator)
        return Subscription.objects.filter(subscribed_to = creator)
    except:
        return []
    
def filter_all_posts(user, creator):
    return Posts.objects.filter(author = user, content_creator = creator)

def filter_latest_post(user, creator):
    try:
        return filter_all_posts(user, creator).latest('created_at')
    except:
        pass

def filter_blocked_users(user):
    try:
        return Blocked_Subscriber.objects.filter(subscribed_to = user)
    except:
        return []