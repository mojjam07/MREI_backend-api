"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return JsonResponse({
        "message": "Welcome to the platform",
        "status": "OK"
    })

def serve_react_app(request):
    """Serve the React app for all non-API routes"""
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    else:
        return HttpResponse("React app not built. Please run 'npm run build' in the frontend directory.", status=404)

urlpatterns = [
    path('', serve_react_app),  # Serve React app for root
    path('admin/', admin.site.urls),
    path('api/', include('config.urls')),
    re_path(r'^(?!api/|admin/|static/|media/).*$', serve_react_app),  # Catch all other routes except API, admin, static, and media
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
