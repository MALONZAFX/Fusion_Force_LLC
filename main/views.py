# views.py - NO DATABASE VERSION
from django.shortcuts import render 
from django.http import JsonResponse
import json

# ============ HOME VIEW ============
def home(request):
    """Home page view - NO DATABASE"""
    
    # HARDCODED DATA - NO DATABASE
    about_content = {
        'title': "Pamela Robinson",
        'description': "Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
        'bullet_points': "Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience\nTrained by Les Brown\nAuthor of Leading with the Heart",
        'image': None
    }
    
    newsletter_content = {
        'title': "Monthly Newsletter",
        'subtitle': "Get exclusive insights and industry updates delivered to your inbox",
        'benefits': "Leadership Strategies\nIndustry Updates\nCase Studies\nEvent Announcements\nExclusive Content\nSuccess Stories",
        'form_title': "Join Our Community",
        'form_description': "Get exclusive leadership insights, industry trends, and event updates delivered directly to your inbox each month."
    }
    
    # Hardcoded services
    services = [
        {'title': 'Keynote Speaking', 'description': 'Inspirational talks for conferences and events', 'icon': '🎤'},
        {'title': 'Leadership Training', 'description': 'Corporate training and team development', 'icon': '👥'},
        {'title': 'Hospitality Consulting', 'description': 'Sales and marketing support for hotels', 'icon': '🏨'},
        {'title': 'Executive Coaching', 'description': 'One-on-one leadership development', 'icon': '💼'},
    ]
    
    # Hardcoded testimonials
    testimonials = [
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
    
    # Duplicate for infinite slider
    duplicated_testimonials = testimonials * 2
    
    context = {
        'about_content': about_content,
        'services': services,
        'testimonials': duplicated_testimonials,
        'events': [],  # Empty for now
        'newsletter_content': newsletter_content,
        'gallery_images': [],  # Empty for now
        'contact_form': None,  # Disable forms for now
        'newsletter_form': None,
        'footer_newsletter_form': None,
    }
    
    return render(request, 'main/index.html', context)

# ============ SIMPLE FORM HANDLERS ============
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
    """About page view - NO DATABASE"""
    about_content = {
        'title': "Pamela Robinson",
        'description': "Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
        'bullet_points': "Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience",
        'image': None
    }
    
    return render(request, 'main/about.html', {'about_content': about_content})