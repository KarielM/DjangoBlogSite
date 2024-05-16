from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import Create_User_Form

# Create your views here.
# def Create_User_View(request:HttpRequest):
#     form = Create_User_Form(request.POST)

#     if form.is_valid():
#         form.save()
#     else:
#         print(form.errors)

#     return render (request, 'register_user.html', {'form':form})

def Create_User_View(request: HttpRequest):
    form = Create_User_Form()

    if request.method == 'POST':
        form = Create_User_Form(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {user}.' )
            return redirect('user_login')

    return render(request, 'register_user.html', {'form': form})

def User_Login_View(request: HttpRequest):
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

def Dashboard_View(request:HttpRequest):
    return render(request, 'dashboard.html')