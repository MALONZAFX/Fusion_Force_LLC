from django.core.management.base import BaseCommand
from main.models import HomeContent, AboutContent, Service, Testimonial, Event

class Command(BaseCommand):
    help = 'Seed initial data for Fusion Force website'
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding initial data...")
        
        # Clear existing data (optional - remove if you want to keep existing)
        self.stdout.write("Clearing existing data...")
        HomeContent.objects.all().delete()
        AboutContent.objects.all().delete()
        Service.objects.all().delete()
        Testimonial.objects.all().delete()
        Event.objects.all().delete()
        
        # Create Home Content
        home_content = HomeContent.objects.create(
            title="Fusion Force LLC",
            subtitle="Pamela Robinson - Making the Impossible Possible through transformative speaking, corporate training, and leadership development.",
            is_active=True
        )
        self.stdout.write(f"âœ“ Created Home Content: {home_content}")
        
        # Create About Content
        about_content = AboutContent.objects.create(
            title="Pamela Robinson",
            description="""Pamela Robinson is a keynote speaker, corporate and leadership trainer,founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies. Her career spans Asia, North America, the United States, and the Caribbean, where she has served as a General Manager, Director of Sales, and consultant for leading hotel operations and hospitality brands.

Pamela's passion for empowering women is the heartbeat of her mission. She began speaking at schools, sharing messages of hope, resilience, and purpose with young women from all walks of life. Through her authentic voice and heartfelt stories, Pamela inspires others to recognize their worth, embrace their unique journeys, and pursue their dreams with confidence. Her work continues to uplift and equip women to rise above challenges and step boldly into their full potential.""",
            bullet_points="""Keynote Speaker
Leadership Trainer
Hospitality Expert
Global Experience
Trained by Les Brown
Author of Leading with the Heart"""
        )
        self.stdout.write(f"âœ“ Created About Content: {about_content}")
        
        # Create Services
        services_data = [
            {
                'title': 'Keynote Speaking',
                'service_type': 'keynote',
                'description': 'Inspire your team with powerful messages that drive action and create lasting change.',
                'icon_class': 'fas fa-microphone',
                'topics': 'Emotional Intelligence, Leadership Trust, Guest Experience, Women in Leadership, Extraordinary Leadership'
            },
            {
                'title': 'Corporate Training',
                'service_type': 'training',
                'description': 'Develop your team with proven frameworks that boost performance and engagement.',
                'icon_class': 'fas fa-users',
                'topics': 'Leadership Training, Customer Service Excellence, Team Collaboration, EQ Training, Workplace Etiquette'
            },
            {
                'title': 'Sales & Marketing Support',
                'service_type': 'consulting',
                'description': 'Specialized support for hospitality businesses seeking to elevate sales and marketing performance.',
                'icon_class': 'fas fa-chart-line',
                'topics': 'Sales Strategy, Increasing Market Share, Hospitality Excellence, Increasing Revenue Growth, Increasing Occupancy'
            },
        ]
        
        for service_data in services_data:
            service = Service.objects.create(**service_data)
            self.stdout.write(f"âœ“ Created Service: {service}")
        
        # Create Testimonials
        testimonials_data = [
            {
                'client_name': 'Event Organizer',
                'position': 'Event Organizer',
                'company': 'IMEX America',
                'content': "Pamela doesn't just speak, she transforms. Her sessions ignite courage, clarity, and connection.",
                'is_active': True
            },
            {
                'client_name': 'Vice President',
                'position': 'Vice President of Sales',
                'company': 'Luxury Hotel Group',
                'content': "Her energy is unmatched, our team left inspired and aligned.",
                'is_active': True
            },
            {
                'client_name': 'Development Director',
                'position': 'Development Director',
                'company': 'Russian Hospitality Awards',
                'content': "Pamela was exceptionally well-spoken, engaging, and demonstrated a deep understanding of the hospitality industry. Her ability to connect with the audience made her session both impactful and memorable.",
                'is_active': True
            },
        ]
        
        for testimonial_data in testimonials_data:
            testimonial = Testimonial.objects.create(**testimonial_data)
            self.stdout.write(f"âœ“ Created Testimonial: {testimonial}")
        
        # Create Events
        events_data = [
            {
                'title': 'Corporate Leadership Summits',
                'description': 'Speaking at major corporate leadership events worldwide.',
                'event_type': 'Leadership Events'
            },
            {
                'title': "Women's Empowerment Conferences",
                'description': 'Empowering women through keynote speeches and workshops.',
                'event_type': 'Empowerment Events'
            },
            {
                'title': 'IMEX AMERICA',
                'description': 'Latest speaking engagement at the premier hospitality industry event.',
                'event_type': 'Latest Event'
            },
        ]
        
        for event_data in events_data:
            event = Event.objects.create(**event_data)
            self.stdout.write(f"âœ“ Created Event: {event}")
        
        self.stdout.write(self.style.SUCCESS('âœ“ All data seeded successfully!'))
