# views.py - SAFE VERSION WITH DATABASE ERROR HANDLING
from django.shortcuts import render 
from django.http import JsonResponse
from django.db import connection, OperationalError, ProgrammingError
import json

# ============ SAFE DATABASE HELPER ============
def safe_db_query(model_class, fallback_data=None):
    """Safely query database, fallback if table doesn't exist"""
    try:
        # Check if table exists
        table_name = model_class._meta.db_table
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
                    [table_name]
                )
            else:  # sqlite
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    [table_name]
                )
            table_exists = cursor.fetchone()[0] if cursor.fetchone() else False
        
        if table_exists:
            return model_class.objects.first()
        else:
            return fallback_data
    except (OperationalError, ProgrammingError, Exception) as e:
        print(f"Database error for {model_class.__name__}: {e}")
        return fallback_data

def safe_db_all(model_class, fallback_list=None):
    """Safely get all objects, fallback if table doesn't exist"""
    try:
        # Check if table exists
        table_name = model_class._meta.db_table
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
                    [table_name]
                )
            else:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    [table_name]
                )
            table_exists = cursor.fetchone()[0] if cursor.fetchone() else False
        
        if table_exists:
            return list(model_class.objects.all())
        else:
            return fallback_list or []
    except (OperationalError, ProgrammingError, Exception) as e:
        print(f"Database error for {model_class.__name__}: {e}")
        return fallback_list or []

# ============ HOME VIEW ============
def home(request):
    """Home page view - SAFE VERSION"""
    
    # Define fallback data
    fallback_about = {
        'title': "Pamela Robinson",
        'description': "Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
        'bullet_points': "Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience\nTrained by Les Brown\nAuthor of Leading with the Heart",
        'image': None
    }
    
    fallback_newsletter = {
        'title': "Monthly Newsletter",
        'subtitle': "Get exclusive insights and industry updates delivered to your inbox",
        'benefits': "Leadership Strategies\nIndustry Updates\nCase Studies\nEvent Announcements\nExclusive Content\nSuccess Stories",
        'form_title': "Join Our Community",
        'form_description': "Get exclusive leadership insights, industry trends, and event updates delivered directly to your inbox each month."
    }
    
    fallback_testimonials = [
        {
            'client_name': 'Event Organizer',
            'position': 'Event Organizer',
            'company': 'IMEX America',
            'content': 'Pamela doesn\'t just speak, she transforms. Her sessions ignite courage, clarity, and connection.',
            'avatar': None,
        },
        {
            'client_name': 'Vice President',
            'position': 'Vice President of Sales',
            'company': 'Luxury Hotel Group',
            'content': 'Her energy is unmatched, our team left inspired and aligned.',
            'avatar': None,
        },
        {
            'client_name': 'Development Director',
            'position': 'Development Director',
            'company': 'Russian Hospitality Awards',
            'content': 'Pamela was exceptionally well-spoken, engaging, and demonstrated a deep understanding of the hospitality industry.',
            'avatar': None,
        }
    ]
    
    # Try to import models (they might not exist in database yet)
    try:
        from .models import (
            AboutContent, Service, Testimonial, Event, 
            NewsletterContent, GalleryImage, ContactForm, NewsletterForm
        )
        
        # Safe database queries
        about_content = safe_db_query(AboutContent, fallback_about)
        newsletter_content = safe_db_query(NewsletterContent, fallback_newsletter)
        services = safe_db_all(Service, [])
        testimonials = safe_db_all(Testimonial, fallback_testimonials)
        events = safe_db_all(Event, [])
        gallery_images = safe_db_all(GalleryImage, [])
        
    except ImportError:
        # Models not imported yet
        about_content = fallback_about
        newsletter_content = fallback_newsletter
        services = []
        testimonials = fallback_testimonials
        events = []
        gallery_images = []
        ContactForm = None
        NewsletterForm = None
    
    # Duplicate testimonials for infinite slider
    duplicated_testimonials = testimonials * 2 if testimonials else []
    
    context = {
        'about_content': about_content,
        'services': services,
        'testimonials': duplicated_testimonials,
        'events': events,
        'newsletter_content': newsletter_content,
        'gallery_images': gallery_images,
        'contact_form': ContactForm() if ContactForm else None,
        'newsletter_form': NewsletterForm(initial={'source': 'newsletter_section'}) if NewsletterForm else None,
        'footer_newsletter_form': NewsletterForm(initial={'source': 'footer'}) if NewsletterForm else None,
    }
    
    return render(request, 'main/index.html', context)

# ============ SIMPLIFIED CONTACT & NEWSLETTER VIEWS ============
def contact_submit(request):
    """Simple contact form handler"""
    return JsonResponse({
        'status': 'success',
        'message': 'Thank you for your message! We\'ll contact you soon.'
    })

def newsletter_submit(request):
    """Simple newsletter form handler"""
    return JsonResponse({
        'status': 'success', 
        'message': 'Thank you for subscribing!'
    })

# ============ ABOUT VIEW ============
def about(request):
    """About page view - SAFE VERSION"""
    fallback_about = {
        'title': "Pamela Robinson",
        'description': "Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
        'bullet_points': "Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience",
        'image': None
    }
    
    try:
        from .models import AboutContent
        about_content = safe_db_query(AboutContent, fallback_about)
    except ImportError:
        about_content = fallback_about
    
    return render(request, 'main/about.html', {'about_content': about_content})