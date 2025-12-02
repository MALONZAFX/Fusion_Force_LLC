# views.py - FIXED WITH ALL IMPORTS
from django.shortcuts import render  # ← CRITICAL: ADD THIS
from django.http import JsonResponse
from .models import (
    HomeContent, AboutContent, Service, 
    Testimonial, Event, NewsletterContent, GalleryImage,
    ContactSubmission, NewsletterSubscription, SystemLog
)
from .forms import ContactForm, NewsletterForm
import json

def log_action(message, level='info', source='views', request=None):
    """Helper function to log actions"""
    try:
        log = SystemLog.objects.create(
            log_level=level,
            message=message,
            source=source,
            user_ip=request.META.get('REMOTE_ADDR') if request else None,
            user_agent=request.META.get('HTTP_USER_AGENT', '') if request else ''
        )
        return log
    except Exception as e:
        print(f"Failed to log: {e}")

def home(request):
    # Get active home content or use default
    home_content = HomeContent.objects.filter(is_active=True).first()
    if not home_content:
        home_content = HomeContent.objects.create(
            title="Fusion Force LLC",
            subtitle="Pamela Robinson - Making the Impossible Possible through transformative speaking, corporate training, and leadership development.",
            is_active=True
        )
    
    # Get about content or create default
    about_content = AboutContent.objects.first()
    if not about_content:
        about_content = AboutContent.objects.create(
            title="Pamela Robinson",
            description="Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
            bullet_points="Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience\nTrained by Les Brown\nAuthor of Leading with the Heart"
        )
    
    # Get newsletter content or create default
    newsletter_content = NewsletterContent.objects.first()
    if not newsletter_content:
        newsletter_content = NewsletterContent.objects.create(
            title="Monthly Newsletter",
            subtitle="Get exclusive insights and industry updates delivered to your inbox",
            benefits="Leadership Strategies\nIndustry Updates\nCase Studies\nEvent Announcements\nExclusive Content\nSuccess Stories",
            form_title="Join Our Community",
            form_description="Get exclusive leadership insights, industry trends, and event updates delivered directly to your inbox each month."
        )
    
    # Get all services
    services = Service.objects.all()
    
    # Get gallery images
    gallery_images = GalleryImage.objects.filter(
        is_active=True
    ).exclude(
        image__isnull=True
    ).exclude(
        image=''
    ).order_by('-display_order', '-created_at')
    
    # Get active testimonials
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Get all events
    events = Event.objects.all()
    
    # Duplicate testimonials for infinite slider effect
    testimonial_list = list(testimonials)
    
    # If no testimonials in database, use defaults
    if not testimonial_list:
        testimonial_list = [
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
    duplicated_testimonials = testimonial_list * 2
    
    context = {
        'home_content': home_content,
        'about_content': about_content,
        'services': services,
        'testimonials': duplicated_testimonials,
        'events': events,
        'newsletter_content': newsletter_content,
        'gallery_images': gallery_images,
        'contact_form': ContactForm(),
        'newsletter_form': NewsletterForm(initial={'source': 'newsletter_section'}),
        'footer_newsletter_form': NewsletterForm(initial={'source': 'footer'}),
    }
    
    return render(request, 'main/index.html', context)

def contact_submit(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            form = ContactForm(data)
            
            if form.is_valid():
                contact = form.save()
                log_action(
                    f"New contact form submission: {contact.full_name} from {contact.organization}",
                    level='success',
                    source='contact_submit',
                    request=request
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you for your booking request! We\'ll contact you within 24 hours.'
                })
            else:
                errors = {field: str(error) for field, error in form.errors.items()}
                log_action(
                    f"Contact form validation failed: {errors}",
                    level='warning',
                    source='contact_submit',
                    request=request
                )
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill all required fields correctly.',
                    'errors': errors
                }, status=400)
                
        except Exception as e:
            log_action(
                f"Contact form submission error: {str(e)}",
                level='error',
                source='contact_submit',
                request=request
            )
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again later.'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)

def newsletter_submit(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            
            # Check if email already exists
            email = data.get('email')
            if NewsletterSubscription.objects.filter(email=email).exists():
                log_action(
                    f"Duplicate newsletter subscription attempt: {email}",
                    level='warning',
                    source='newsletter_submit',
                    request=request
                )
                return JsonResponse({
                    'status': 'info',
                    'message': 'You are already subscribed to our newsletter!'
                })
            
            form = NewsletterForm(data)
            
            if form.is_valid():
                subscription = form.save()
                log_action(
                    f"New newsletter subscription: {subscription.email} from {subscription.get_source_display()}",
                    level='success',
                    source='newsletter_submit',
                    request=request
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you for subscribing to our newsletter!'
                })
            else:
                errors = {field: str(error) for field, error in form.errors.items()}
                log_action(
                    f"Newsletter form validation failed: {errors}",
                    level='warning',
                    source='newsletter_submit',
                    request=request
                )
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please provide a valid email address.',
                    'errors': errors
                }, status=400)
                
        except Exception as e:
            log_action(
                f"Newsletter submission error: {str(e)}",
                level='error',
                source='newsletter_submit',
                request=request
            )
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again later.'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)

def about(request):
    about_content = AboutContent.objects.first()
    if not about_content:
        about_content = AboutContent.objects.create(
            title="Pamela Robinson",
            description="Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
            bullet_points="Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience"
        )
    return render(request, 'main/about.html', {'about_content': about_content})