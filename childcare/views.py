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
,,,,