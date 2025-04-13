from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
import uuid
from django.utils.timezone import now
from datetime import timedelta

# Create your views here.
def Home(request):
    return render(request, 'home.html')


def signup_parent(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup_parent')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('signup_parent')

        user = User.objects.create_user(username=username, email=email, password=password)
        Parent.objects.create(user=user, phone=phone)
        login(request, user)
        return redirect('home')

    return render(request, 'auth/signup_parent.html')