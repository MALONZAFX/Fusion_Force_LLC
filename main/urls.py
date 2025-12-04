from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('team/', views.team, name='team'),
    path('testimonials/', views.testimonial_view, name='testimonials'),
    path('courses/', views.courses, name='courses'),
    
    # Form submission endpoints
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/subscribe/', views.newsletter_submit, name='newsletter_subscribe'),
]