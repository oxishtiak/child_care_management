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

def signup_staff(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        is_staff = 'is_staff' in request.POST
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup_staff')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('signup_staff')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Staff.objects.create(user=user, mobile=mobile,is_staff=is_staff, is_active=True)
        messages.success(request, 'Staff registration is successful')
        return redirect('staff_login')
    
    return render(request, 'auth/signup_staff.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'auth/login.html')

def staff_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'auth/staff_login.html')



@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def staff_logout(request):
    logout(request)
    return redirect('home')

@login_required (login_url='staff_login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


# Parent Dashboard

@login_required(login_url='login')
def parent_profile(request):
    parent = get_object_or_404(Parent, user=request.user)
    children = parent.children.all()
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        parent.phone = phone
        parent.address = address
        parent.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('parent_profile')
    
    return render(request, 'profile/parent_profile.html', {'parent': parent, 'children': children})

@login_required(login_url='login')
def add_child(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        dob = request.POST['date_of_birth']
        image = request.FILES.get('image')
        
        parent = get_object_or_404(Parent, user=request.user)
        Child.objects.create(
            parent=parent, name=name, age=age, date_of_birth=dob, image=image, unique_id=uuid.uuid4()
        )
        messages.success(request, 'Child added successfully!')
        return redirect('parent_profile')
    
    return render(request, 'profile/add_child.html')

@login_required(login_url='login')
def edit_child(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent__user=request.user)
    
    if request.method == 'POST':
        child.name = request.POST['name']
        child.age = request.POST['age']
        child.date_of_birth = request.POST['date_of_birth']
        if 'image' in request.FILES:
            child.image = request.FILES['image']
        child.save()
        messages.success(request, 'Child updated successfully!')
        return redirect('parent_profile')
    
    return render(request, 'profile/edit_child.html', {'child': child})

@login_required(login_url='login')
def delete_child(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent__user=request.user)
    child.delete()
    messages.success(request, 'Child deleted successfully!')
    return redirect('parent_profile')


# Package Views
def packages(request):
    packages = Package.objects.filter(is_active=True)
    return render(request, 'package.html', {'packages': packages})


# Booking Views
@login_required(login_url='login')
def booking(request, package_id):
    parent = get_object_or_404(Parent, user=request.user)
    children = Child.objects.filter(parent=parent)
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        selected_children_ids = request.POST.getlist('children')  # Get list of selected children
        start_date = request.POST.get('start_date')

        if not selected_children_ids:
            messages.error(request, "Please select at least one child.")
            return redirect('booking', package_id=package_id)

        # Create the booking
        booking = Booking.objects.create(
            parent=parent,
            package=package,
            total_price=package.price,
            start_date=start_date,
            end_date=now().date() + timedelta(days=package.duration_days),
            status="pending",
            is_paid=False
        )
        booking.children.set(selected_children_ids)

        messages.success(request, "Booking initiated. Proceed to checkout.")
        return redirect('checkout', booking_id=booking.id)

    return render(request, 'booking/booking.html', {'package': package, 'children': children})


# Checkout Views
@login_required(login_url='login')
def checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, parent__user=request.user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method not in ['card', 'bkash', 'nagad', 'cash']:
            messages.error(request, "Invalid payment method selected.")
            return redirect('checkout', booking_id=booking.id)

       
        transaction = Transaction.objects.create(
            booking=booking,
            payment_method=payment_method,
            transaction_id=uuid.uuid4(),
            is_successful=True
        )

        # Update booking status to confirmed
        booking.is_paid = True
        booking.status = "confirmed"
        booking.save()

        messages.success(request, "Payment successful! Your booking is confirmed.")
        return redirect('my_bookings')

    return render(request, 'booking/checkout.html', {'booking': booking})


# My Bookings Views
@login_required(login_url='login')
def my_bookings(request):
    parent = get_object_or_404(Parent, user=request.user)
    bookings = Booking.objects.filter(parent=parent).order_by('-created_at')

    return render(request, 'booking/my_bookings.html', {'bookings': bookings})