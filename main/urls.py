# urls.py (app level)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    # Form submission endpoints
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/subscribe/', views.newsletter_submit, name='newsletter_subscribe'),
]
