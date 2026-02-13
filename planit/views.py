from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import AppUser, Event, EventImage, EventAttendance
from django.utils import timezone
from django.utils.dateparse import parse_datetime

#   --------------------------------------------------------    LOGIN / SINGUP

#   --- PÁGINA DE LOGIN
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
            messages.success(request, f'¡ Bienvenido, {user.first_name or user.username} !')
            next_url = request.GET.get('next','home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario / Email Inválido.')
    return render(request, 'login.html')

#   --- LOGOUT
def logout_view(request):
    logout(request)
    messages.success(request, 'Se ha Cerrado su Sesión correctamente.')
    return redirect('home')

#   --- PÁGINA DE REGISTRO
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
        
        if len(password) < 8:
            messages.error(request, 'Contraseña debe tener más de 8 caracteres.')
            return render(request, 'signup.html')
        
        if password != password_confirm:
            messages.error(request, 'Las Contraseñas no son iguales.')
            return render(request, 'signup.html')
        
        if AppUser.objects.filter(username=username).exists():
            messages.error(request, 'Usuario ya existe.')
            return render(request, 'signup.html')
        
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, 'email ya existe.')
            return render(request, 'signup.html')
        
        if telephone and AppUser.objects.filter(telephone=telephone).exists():
            messages.error(request, 'Número de Teléfono ya existe.')
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
            messages.success(request, f'¡ Bienvenido a Planit, {user.first_name} !')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error Creando Cuenta: {str(e)}')
    
    return render(request, 'signup.html')
#   --------------------------------------------------------

#   --------------------------------------------------------    PÁGINAS PRINCIPALES

#   --- PÁGINA DE INICIO
def home(request):
    events = Event.objects.all().order_by('-id')[:3]
    
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

#   --- PÁGINA DE LISTA DE EVENTOS
def events_list(request):
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        events = Event.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by('-date_start')
    else:
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
    
    context = {
        'events_data': events_data,
        'search_query': search_query,
    }
    return render(request, 'events_list.html', context)

#   --- PÁGINA DE DETALLE DE EVENTO
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

#   --------------------------------------------------------

#   --------------------------------------------------------    CRUD EVENTOS

#   --- PÁGINA DE CREAR EVENTO
@login_required
def create_event(request):
    if request.method == 'POST':
        
        date_start_str = request.POST.get('date_start')
        date_start = parse_datetime(date_start_str)

        if not date_start:
            messages.error(request, "Formato de Fecha Inválido.")
            return render(request, 'create_event.html')

        if timezone.is_naive(date_start):
            date_start = timezone.make_aware(date_start, timezone.get_current_timezone())

        if date_start <= timezone.now():
            messages.error(request, "La Fecha del Evento debe ser futura.")
            return render(request, 'create_event.html')

        event = Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            slots=request.POST.get('slots'),
            date_start=date_start,
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
        
        messages.success(request, f'Evento "{event.title}" creado con éxito!')
        return redirect('event_detail', pk=event.pk) 
    
    return render(request, 'create_event.html', {'now' : timezone.now()})

#   --- ATENDER EVENTO
@login_required
def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.creator == request.user:
        messages.error(request, "No puedes asistir a tu propio Evento.")
        return redirect('event_detail', pk=pk)
    
    if event.attendees.filter(pk=request.user.pk).exists():
        messages.warning(request, "Ya estás asitiendo a este Evento.")
        return redirect('event_detail', pk=pk)
    
    attendees_count = event.attendees.count()
    if attendees_count >= event.slots:
        messages.error(request, "Evento Lleno. No hay espacios disponibles.")
        return redirect('event_detail', pk=pk)
    
    EventAttendance.objects.create(event=event, user=request.user)
    messages.success(request, f"¡ Vas a Asistir a '{event.title}' !")
    return redirect('event_detail', pk=pk)

#   --- CANCELAR ASISTENCIA
@login_required
def cancel_attendance(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    EventAttendance.objects.filter(event=event, user=request.user).delete()
    messages.success(request, f"Asistencia Cancelada para '{event.title}'.")
    return redirect('event_detail', pk=pk)

#   --- PÁGINA DE EDITAR EVENTO
@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.creator != request.user:
        messages.error(request, "No tienes permiso para editar este Evento.")
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        
        date_start_str = request.POST.get('date_start')
        if not date_start_str:
            messages.error(request, "Fecha es obligatoria.")
            return render(request, 'edit_event.html', {'event': event, 'now': timezone.now()})

        date_start = parse_datetime(date_start_str)

        if not date_start:
            messages.error(request, "Formato de Fecha incorrecto.")
            return render(request, 'edit_event.html', {'event': event, 'now': timezone.now()})

        if timezone.is_naive(date_start):
            date_start = timezone.make_aware(
                date_start,
                timezone.get_current_timezone()
            )

        if date_start <= timezone.now():
            messages.error(request, "La Fecha del Evento debe ser futura.")
            return render(request, 'edit_event.html', {'event': event, 'now': timezone.now()})
        
        attendees_count = event.attendees.count()
        new_slots = int(request.POST.get('slots'))
        
        if new_slots < attendees_count:
            messages.error(request, f'Espacios disponibles no pueden ser menor que el número de gente asistiendo.')
            return render(request, 'edit_event.html', {'event': event, 'now': timezone.now()})
        
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.slots = request.POST.get('slots')
        event.date_start = date_start
        event.save()
        
        images = request.FILES.getlist('images')
        if images:
            current_max_order = event.images.count() # type: ignore
            for index, image in enumerate(images):
                caption = request.POST.get(f'caption_{index}', '')
                EventImage.objects.create(
                    event=event,
                    image=image,
                    caption=caption,
                    order=current_max_order + index
                )
        
        messages.success(request, f'¡ Evento "{event.title}" actualizado con éxito !')
        return redirect('event_detail', pk=event.pk)
    return render(request, 'edit_event.html', {'event': event, 'now' : timezone.now()})

#   --- ELIMINAR IMAGEN EVENTO
@login_required
def delete_event_image(request, pk, image_id):
    event = get_object_or_404(Event, pk=pk)
    image = get_object_or_404(EventImage, pk=image_id, event=event)
    
    if event.creator != request.user:
        messages.error(request, "No tienes permiso para editar este Evento.")
        return redirect('event_detail', pk=pk)
    
    image.delete()
    messages.success(request, "Imagen eliminada con éxito.")
    return redirect('edit_event', pk=pk)

#   --- ELIMINAR EVENTO
@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.creator != request.user:
        messages.error(request, "No tienes permiso para eliminar este Evento.")
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Evento "{event_title}" eliminado con éxito.')
        return redirect('home')
    
    return redirect('event_detail', pk=pk)

#   --------------------------------------------------------

#   --------------------------------------------------------    CRUD USUARIO

#   --- PÁGINA DE PERFIL
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

#   --- PÁGINA DE AJUSTES DE PERFIL
@login_required
def profile_settings(request):
    if request.method == 'POST':
        user = request.user
        
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone', '')
        age = request.POST.get('age', 0)
        
        if username != user.username and AppUser.objects.filter(username=username).exists():
            messages.error(request, 'Usuario ya existe.')
            return render(request, 'profile_settings.html')
        
        if email != user.email and AppUser.objects.filter(email=email).exists():
            messages.error(request, 'Email ya existe.')
            return render(request, 'profile_settings.html')
        
        if telephone and telephone != user.telephone and AppUser.objects.filter(telephone=telephone).exists():
            messages.error(request, 'Número de Teléfono ya existe.')
            return render(request, 'profile_settings.html')
        
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.telephone = telephone
        user.age = int(age) if age else 0
        
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if current_password or new_password or confirm_password:
            
            if not current_password:
                messages.error(request, 'Por favor introduzca su Contraseña Actual para cambiarla.')
                return render(request, 'profile_settings.html')
            
            if not user.check_password(current_password):
                messages.error(request, 'Contraseña Actual es incorrecta.')
                return render(request, 'profile_settings.html')
            
            if new_password != confirm_password:
                messages.error(request, 'Nuevas Contraseñas no son iguales.')
                return render(request, 'profile_settings.html')
            
            if len(new_password) < 8:
                messages.error(request, 'Nueva Contraseña debe tener más de 8 caracteres.')
                return render(request, 'profile_settings.html')
            
            user.set_password(new_password)
            messages.success(request, '¡ Perfil actualizado con éxito !')
            user.save()
            logout(request)
            return redirect('login')
        
        user.save()
        messages.success(request, '¡ Perfil actualizado con éxito !')
        return redirect('profile')
    
    return render(request, 'profile_settings.html')

#   --- ELIMINAR USUARIO
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        
        if user.check_password(password):
            logout(request)
            user.delete()
            messages.success(request, 'Cuenta Eliminada con éxito.')
            return redirect('home')
        else:
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('profile_settings')
    
    return redirect('profile_settings')

#   --------------------------------------------------------

#   --------------------------------------------------------    PÁGINA 404

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)