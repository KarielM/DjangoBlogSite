from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class YouTuber(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to')

class Tag(models.Model):
    name = models.CharField(max_length=25)

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    creator = models.ForeignKey(YouTuber, on_delete=models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, null = True)

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete = models.CASCADE)
    subscribed_to = models.ForeignKey(YouTuber, on_delete = models.CASCADE)

class Blocked_Subscriber(models.Model):
    #Fields: ID, blocker (foreign key to VTuber), blocked_user (foreign key to User), date_blocked, etc.
    subscriber = models.ForeignKey(User, on_delete = models.CASCADE)
    subscribed_to = models.ForeignKey(YouTuber, on_delete = models.CASCADE)


############################Creation Models########################
def create_YouTuber(name, subscribers):
    pass


def create_posts(subscriber, creator, post, tags):
    #dynamic input fields w/ plus mark
    #on submit collect all tags and pass them to create_posts as a list
    new_post = Posts.objects.create(user = subscriber
                                ,creator = creator
                                ,post = post 
                                )
    for name in tags:
        new_tag = Tag.objects.get_or_create(name = name)

        new_post.tags.add(new_tag)

def create_Subscription(subscriber, creator):
    return Subscription.objects.create(subscriber = subscriber
                                ,subscribed_to = creator)

def create_Blocked_Subscriber(subscriber, creator):
    return Blocked_Subscriber.objects.create(subscriber = subscriber
                                             ,subscribed_to = creator)

############################Read Models########################

############################Update Models########################

############################Delete Models########################

############################Filter Models########################