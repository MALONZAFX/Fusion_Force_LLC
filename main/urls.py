from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    
    # API endpoints for form submissions
    path('api/contact-submit/', views.contact_submit, name='contact_submit'),
    path('api/newsletter-submit/', views.newsletter_submit, name='newsletter_submit'),
    path('api/formsubmit-webhook/', views.form_submit_webhook, name='formsubmit_webhook'),
    
    # Other pages
    path('about/', views.about_page, name='about'),
    path('services/', views.services_page, name='services'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('testimonials/', views.testimonials_page, name='testimonials'),
    path('contact/', views.contact_page, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error handlers
handler404 = views.handler404
handler500 = views.handler500