"""fusion_force URL Configuration"""
from django.urls import path
from django.views.generic import RedirectView
from main import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Form handlers
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/submit/', views.newsletter_submit, name='newsletter_submit'),
    
    # Comment out admin for now:
    # path('admin/', admin.site.urls),
    
    # Redirect everything else to home
    path('<path:path>/', RedirectView.as_view(url='/')),
]