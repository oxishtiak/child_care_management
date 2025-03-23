"""
URL configuration for CORE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from childcare.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', Home, name='home'),

    path('signup_parent/', signup_parent, name='signup_parent'),
    path('signup_staff/', signup_staff, name='signup_staff'),
    path('login/', user_login, name='login'),
    path('staff_login/', staff_login, name='staff_login'),
    path('logout/', user_logout, name='logout'),
    path('staff_logout/', staff_logout, name='staff_logout'),
    path('package/', packages, name='package'),

    # Parent Urls
    path('parent/profile/', parent_profile, name='parent_profile'),
    path('parent/child/add/', add_child, name='add_child'),
    path('parent/child/edit/<int:child_id>/', edit_child, name='edit_child'),
    path('parent/child/delete/<int:child_id>/', delete_child, name='delete_child'),

    # Booking Urls
    path('book/<int:package_id>/', booking, name='booking'),
    path('checkout/<int:booking_id>/', checkout, name='checkout'),
    path('my-bookings/', my_bookings, name='my_bookings'),

    # Dashboard Staff Urls
    path('dashboard/', dashboard, name='dashboard'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()