from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import *
from .models import *

def Create_User_View(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = Create_User_Form(request.POST)

    if form.is_valid():
        form.save()
        
        user = form.cleaned_data.get('username')
        messages.success(request, f'Account successfully created for {user}.' )
        return redirect('user_login')
    else:
        messages.info(request, form.errors)

    return render(request, 'register_user.html', {'form': form})

def User_Login_View(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Incorrect username and password combination')

        return render(request, 'user_login.html')

def User_Logout_View(request:HttpRequest):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def Dashboard_View(request:HttpRequest):
    subscribers = [user for user in find_all_subscribers(request.user)]
    posts = []
    for user in subscribers:
        youTuber = user.subscribed_to
        user = user.subscriber
        temp_post = filter_latest_post(user, youTuber)
        if temp_post is not None:
            posts.append(filter_latest_post(user, youTuber))
    
    posts = sorted(posts, key =lambda q: q.created_at, reverse=True)
    print(posts)
    try:
        user = YouTuber.objects.get(creator = request.user)
        role = view_role(request.user)
        if role.name == 'Admin':
            return render(request, 'dashboard.html', {'role':role, 'blogs':posts})
    except YouTuber.DoesNotExist:
        return render(request, 'dashboard.html')


@login_required(login_url='user_login')
def create_blog_post_view(request):
    form = Create_Blog_Post_Form(user=request.user)

    if request.method == 'POST':
        form = Create_Blog_Post_Form(request.POST, user=request.user)
        if form.is_valid():
            author = request.user
            title = form.cleaned_data['title']
            content_creator_username = form.cleaned_data['content_creator']
            post = form.cleaned_data['post']

            result = create_posts(author, title, content_creator_username, post)

            if isinstance(result, str):
                messages.error(request, result)
            else:
                messages.success(request, 'Post successfully created')
                return redirect('dashboard')
        else:
            print(form.errors)

    return render(request, 'create_post.html', {'form': form})



@login_required(login_url='user_login')
def view_all_blogs(request):
    posts = view_all_posts(request.user)
    posts = sorted(posts, key =lambda q: q.created_at, reverse=True)
    try:
        users_posts = view_all_posts_associated(YouTuber.objects.get(creator__username = request.user))
        users_posts = sorted(users_posts, key =lambda q: q.created_at, reverse=True)
    except:
        users_posts = []

    if 'user_post' in request.POST:
        if request.method == 'POST':
            post = request.POST.get('user_post')
            user, title = post.split(" ", 1)
            user = User.objects.get(username = user)
            youtuber = YouTuber.objects.get(creator = request.user)

            blog = view_single_blog_reverse_lookup(user, title, youtuber)
            delete_post(blog.title, blog.author)
            

    return render(request, 'view_blogs.html', {'posts': posts, 'users_posts':users_posts})


@login_required(login_url='user_login')
def update_certain_blog_view(request, title, author):
    post = Posts.objects.get(title = title)
    form = Update_Blog_Post_Form(instance=post)
    

    if request.method == 'POST':
        form = Update_Blog_Post_Form(request.POST)
        
        if form.is_valid():
            # print(posts)

            new_title = form.cleaned_data['title'] if post.title != form.cleaned_data['title'] and new_title not in [i.title for i in Posts.objects.filter(author = request.user)]else post.title
            new_post = form.cleaned_data['post'] if post.post != form.cleaned_data['post'] else post.post
            update_certain_post(title, new_title, new_post, post.content_creator)
            return redirect('view_my_blogs')

    return render(request, 'update_blog.html', {'form': form})

@login_required(login_url='user_login')
def delete_post_view(request, title, author):
    # role = UserProfile.objects.get(user = request.user).role
    # post = Posts.objects.get(title = title, author = author, content_creator = YouTuber.objects.get(creator=request.user))
    # print(request.user)
    if request.method == 'POST':
        if request.user.username != author:
            author = User.objects.get(username = author)
            user = YouTuber.objects.get(creator = request.user)
            
            delete_post(title, author, user)
        else:
            content_creator = Posts.objects.get(title = title, author = request.user).content_creator
            # print(content_creator)
            # user = User.objects.get(username = request.user.username)
            # print(request.user.username)
            delete_post(title, request.user, content_creator)
        return redirect('view_my_blogs')

    return render(request, 'delete_blog.html', {'title': title})

@login_required(login_url='user_login')
def subscribe_to_new_user_view(request):
    users_who_blocked_user = [user.subscribed_to for user in view_all_blocked(User.objects.get(username = request.user))]
    users_who_blocked_user = [User.objects.get(username = user) for user in users_who_blocked_user]
    # print(users_who_blocked_user)
    youTuber_list = [user.creator for user in view_all_youTubers() if user.creator != request.user and user.creator not in users_who_blocked_user]
    # print(youTuber_list)
    already_subscribed = [user.subscribed_to.creator for user in filter_all_subscriptions(request.user)]
    available_list = [user for user in youTuber_list if user not in already_subscribed]
    subscribers = [user for user in find_all_subscribers(request.user)]
    role = UserProfile.objects.get(user__username = request.user)
    role = role.role.name
    try:
        blocked_users = filter_blocked_users(YouTuber.objects.get(creator__username = request.user))
    except:
        blocked_users = []
    if request.method == 'POST':
        if 'subscribe_username' in request.POST:
            creator = request.POST.get('subscribe_username')
            print(youTuber_list)
            youTuber = YouTuber.objects.get(creator__username=creator)
            # print(request.POST)
            # print(creator)
            # print(youTuber)
            create_Subscription(request.user, youTuber)
        elif 'unsubscribe_username' in request.POST:
            print(request.POST)
            creator = request.POST.get('unsubscribe_username')
            print(youTuber_list)
            # print(already_subscribed)
            # print(creator)
            youTuber = YouTuber.objects.get(creator__username = creator)
            # print(youTuber)
            print(request.user)
            delete_subscription(request.user, youTuber)
        elif 'block' in request.POST:
            user = User.objects.get(username = request.POST.get('block'))
            youtuber = YouTuber.objects.get(creator__username=request.user)

            create_blocked_user(user, youtuber)
            delete_subscription(user, youtuber)
        elif 'unblock' in request.POST:
            user = User.objects.get(username = request.POST.get('unblock'))
            youtuber = YouTuber.objects.get(creator__username = request.user)

            delete_or_unblock_blocked_user(user, youtuber)

        return redirect('subscribe')
    # return render(request, 'subscribe_new.html', {'youTubers':available_list})
    return render(request, 'subscribe_new.html', {'youTubers':available_list, 'already_subscribed':already_subscribed, 'subscribers':subscribers, 'blocked_users':blocked_users, 'role':role})