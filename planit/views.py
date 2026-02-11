from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AppUser, Event, EventImage

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = AppUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except AppUser.DoesNotExist:
            user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next','main')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email/username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main')

def singup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('telephone', '')
        age = request.POST.get('age', 0)
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')
        
        if AppUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')
        
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'signup.html')
        
        if telephone and AppUser.objects.filter(telephone=telephone).exists():
            messages.error(request, 'Telephone number already exists.')
            return render(request, 'signup.html')
        
        try:
            user = AppUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                age=int(age) if age else 0
            )
            user.set_password(password)
            user.save()
            
            login(request, user)
            messages.success(request, f'Welcome to Planit, {user.first_name}!')
            return redirect('main')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'signup.html')

def main_page(request):
    return render(request, 'main.html')

def create_event(request):
    if request.method == 'POST':
        event = Event.objects.create(
            title=request.POST['title'],
            creator=request.user,
        )
        for image in request.FILES.getlist('images'):
            EventImage.objects.create(
                event=event,
                image=image
            )
