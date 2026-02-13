from django.contrib import admin
from django.urls import path
from planit import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'planit.views.custom_404'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events_list, name='events_list'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.singup_page, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/delete', views.delete_account, name="delete_account"),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/attend/', views.attend_event, name='attend_event'),
    path('event/<int:pk>/cancel/', views.cancel_attendance, name='cancel_attendance'),
    path('event/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:pk>/image/<int:image_id>/delete/', views.delete_event_image, name='delete_event_image'),
    path('create_event',views.create_event, name='create_event'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
