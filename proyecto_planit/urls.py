from django.contrib import admin
from django.urls import path
from planit import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.singup_page, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
