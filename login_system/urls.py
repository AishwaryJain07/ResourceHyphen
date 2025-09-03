"""
URL configuration for login_system project.
v1.1 - Main URL routing with app includes and media serving
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_redirect(request):
    """Redirect authenticated users to appropriate dashboard"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:admin_dashboard')
        else:
            return redirect('dashboard:user_dashboard')
    return redirect('accounts:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('documents.urls')),
    path('accounts/', include('allauth.urls')),  # Django-allauth URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)