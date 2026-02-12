from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AppUser, Event, EventImage, EventAttendance

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
            next_url = request.GET.get('next','home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email/username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

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
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'signup.html')

def home(request):
    events = Event.objects.all().order_by('-date_start')
    
    events_data = []
    for event in events:
        attendees_count = event.attendees.count()
        slots_available = event.slots - attendees_count
        events_data.append({
            'event': event,
            'slots_available': slots_available,
            'attendees_count': attendees_count,
        })
    
    return render(request, 'home.html', {'events_data': events_data})

@login_required
def create_event(request):
    if request.method == 'POST':

        event = Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            slots=request.POST.get('slots'),
            date_start=request.POST.get('date_start'),
            creator=request.user
        )
        
        images = request.FILES.getlist('images')
        for index, image in enumerate(images):
            caption = request.POST.get(f'caption_{index}', '')
            EventImage.objects.create(
                event=event,
                image=image,
                caption=caption,
                order=index
            )
        
        messages.success(request, f'Event "{event.title}" created successfully!')
        return redirect('event_detail', pk=event.pk) 
    
    return render(request, 'create_event.html')

@login_required
def profile(request):
    created_events = request.user.created_events.all().order_by('-date_created')
    attending_events = request.user.attending_events.all().order_by('date_start')
    
    context = {
        'user_obj': request.user,
        'created_events': created_events,
        'attending_events': attending_events,
    }
    return render(request, "profile.html", context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    attendees = event.attendees.all()
    attendees_count = attendees.count()
    slots_available = event.slots - attendees_count
    
    is_attending = False
    is_creator = False
    if request.user.is_authenticated:
        is_attending = attendees.filter(pk=request.user.pk).exists()
        is_creator = event.creator == request.user
    
    context = {
        'event': event,
        'attendees': attendees,
        'attendees_count': attendees_count,
        'slots_available': slots_available,
        'is_attending': is_attending,
        'is_creator': is_creator,
    }
    return render(request, 'event_detail.html', context)

@login_required
def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.creator == request.user:
        messages.error(request, "You cannot attend your own event.")
        return redirect('event_detail', pk=pk)
    
    if event.attendees.filter(pk=request.user.pk).exists():
        messages.warning(request, "You are already attending this event.")
        return redirect('event_detail', pk=pk)
    
    attendees_count = event.attendees.count()
    if attendees_count >= event.slots:
        messages.error(request, "This event is full. No slots available.")
        return redirect('event_detail', pk=pk)
    
    EventAttendance.objects.create(event=event, user=request.user)
    messages.success(request, f"You are now attending '{event.title}'!")
    return redirect('event_detail', pk=pk)

@login_required
def cancel_attendance(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    EventAttendance.objects.filter(event=event, user=request.user).delete()
    messages.success(request, f"You have cancelled your attendance for '{event.title}'.")
    return redirect('event_detail', pk=pk)
