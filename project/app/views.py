from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.
# def Create_User_View(request:HttpRequest):
#     form = Create_User_Form(request.POST)

#     if form.is_valid():
#         form.save()
#     else:
#         print(form.errors)

#     return render (request, 'register_user.html', {'form':form})

def Create_User_View(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = Create_User_Form(request.POST)

    if form.is_valid():
        form.save()
        
        user = form.cleaned_data.get('username')
        messages.success(request, f'Account successfully created for {user}.' )
        return redirect('user_login')

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
                # return redirect('user_login')

        return render(request, 'user_login.html')

def User_Logout_View(request:HttpRequest):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def Dashboard_View(request:HttpRequest):
    role = view_role(request.user)
    if role is not None:
        return render(request, 'dashboard.html', {'role':role})
    else:
        return render(request, 'dashboard.html')


@login_required(login_url='user_login')
def create_blog_post_view(request):
    form = Create_Blog_Post_Form()

    if request.method == 'POST':
        form = Create_Blog_Post_Form(request.POST)
        if form.is_valid():
            # form.save()

            author = request.user
            title = form.cleaned_data['title']
            content_creator_username = form.cleaned_data['content_creator']
            content_creator = YouTuber.objects.get(creator__username=content_creator_username)
            post = form.cleaned_data['post']  

            # create_posts(author, content_creator, post, title) 
            create_posts(author, title, content_creator, post)
            messages.success(request, 'Post successfully created')         

            # create_posts(form.cleaned_data)
            return redirect('dashboard')

    return render(request, 'create_post.html', {'form': form})


@login_required(login_url='user_login')
def view_all_blogs(request):
    user = request.user
    posts = view_all_posts(user)
    return render(request, 'view_blogs.html', {'posts': posts})


@login_required(login_url='user_login')
def update_certain_blog_view(request, title):
    post = Posts.objects.get(title = title)
    form = Update_Blog_Post_Form(instance=post)

    if request.method == 'POST':
        form = Update_Blog_Post_Form(request.POST)
        
        if form.is_valid():

            user = request.user
            new_title = form.cleaned_data['title'] if post.title != form.cleaned_data['title'] else post.title
            new_post = form.cleaned_data['post'] if post.post != form.cleaned_data['post'] else post.post
            update_certain_post(title, new_title, new_post, post.content_creator)

            return redirect('dashboard')

    return render(request, 'update_blog.html', {'form': form})

@login_required(login_url='user_login')
def delete_post_view(request, title):
    if request.method == "POST":
        user = request.user

        delete_post(title, user)
        return redirect('view_my_blogs')
    return render(request, 'delete_blog.html', {'title': title})