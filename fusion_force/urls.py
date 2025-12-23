from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),  # REGULAR ADMIN URL - DON'T CHANGE
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



def health_check(request):
    return JsonResponse({"status": "healthy", "service": "fusion_force"}, status=200)

urlpatterns = [
    # THIS LINE IS CRITICAL
   path('health', health_check, name='health-check'), 
    
    # Your existing URLs
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Your main app
]
