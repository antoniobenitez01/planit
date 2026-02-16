from django.contrib import admin
from django.urls import path
from planit import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'planit.views.custom_404'                                                                          #   PÁGINA 404

urlpatterns = [
    path('', views.home, name='home'),                                                                          #   INICIO
    path('events/', views.events_list, name='events_list'),                                                     #   LISTA DE EVENTOS
    path('login/', views.login_page, name='login'),                                                             #   LOGIN
    path('signup/', views.singup_page, name='signup'),                                                          #   REGISTRO
    path('logout/', views.logout_view, name='logout'),                                                          #   CERRAR SESIÓN
    path('profile/', views.profile, name='profile'),                                                            #   PERFIL
    path('profile/settings/', views.profile_settings, name='profile_settings'),                                 #   AJUSTES DE PERFIL
    path('profile/delete', views.delete_account, name="delete_account"),                                        #   BORRAR USUARIO
    path('event/<int:pk>/', views.event_detail, name='event_detail'),                                           #   DETALLE DE EVENTO
    path('event/<int:pk>/attend/', views.attend_event, name='attend_event'),                                    #   ATENDER EVENTO
    path('event/<int:pk>/cancel/', views.cancel_attendance, name='cancel_attendance'),                          #   CANCELAR ASISTENCIA
    path('event/<int:pk>/edit/', views.edit_event, name='edit_event'),                                          #   EDITAR EVENTO
    path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),                                    #   ELIMINAR EVENTO
    path('event/<int:pk>/finish/', views.finish_event, name='finish_event'),                                    #   FINALIZAR EVENTO
    path('event/<int:pk>/image/<int:image_id>/delete/', views.delete_event_image, name='delete_event_image'),   #   ELIMINAR IMAGEN EVENTO
    path('create_event',views.create_event, name='create_event'),                                               #   CREAR EVENTO
    path('admin/', admin.site.urls),                                                                            #   /!\ ADMIN
]

#   --- DEBUG - Establece la dirección estática donde se suben las Imágenes de Evento
if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
