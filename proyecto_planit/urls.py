from django.contrib import admin
from django.urls import path
from planit import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.singup_page, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/attend/', views.attend_event, name='attend_event'),
    path('event/<int:pk>/cancel/', views.cancel_attendance, name='cancel_attendance'),
    path('create_event',views.create_event, name='create_event'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
