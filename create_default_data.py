from django.core.management.base import BaseCommand
from main.models import HomeContent, AboutContent, Service, Testimonial, Event

class Command(BaseCommand):
    help = 'Create default data for the website'
    
    def handle(self, *args, **kwargs):
        # Create default home content
        if not HomeContent.objects.exists():
            HomeContent.objects.create(
                title="Fusion Force LLC",
                subtitle="Pamela Robinson - Making the Impossible Possible through transformative speaking, corporate training, and leadership development.",
                is_active=True
            )
        
        # Create default about content
        if not AboutContent.objects.exists():
            AboutContent.objects.create(
                title="Pamela Robinson",
                description="Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.",
                bullet_points="Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience\nTrained by Les Brown\nAuthor of Leading with the Heart"
            )
        
        # Create default services
        if not Service.objects.exists():
            Service.objects.create(
                title="Keynote Speaking",
                service_type="keynote",
                description="Inspire your team with powerful messages that drive action and create lasting change.",
                icon_class="fas fa-microphone",
                topics="Emotional Intelligence, Leadership Trust, Guest Experience, Women in Leadership, Extraordinary Leadership"
            )
            Service.objects.create(
                title="Corporate Training",
                service_type="training",
                description="Develop your team with proven frameworks that boost performance and engagement.",
                icon_class="fas fa-users",
                topics="Leadership Training, Customer Service Excellence, Team Collaboration, EQ Training, Workplace Etiquette"
            )
            Service.objects.create(
                title="Sales & Marketing Support",
                service_type="consulting",
                description="Specialized support for hospitality businesses seeking to elevate sales and marketing performance.",
                icon_class="fas fa-chart-line",
                topics="Sales Strategy, Increasing Market Share, Hospitality Excellence, Increasing Revenue Growth, Increasing Occupancy"
            )
        
        self.stdout.write(self.style.SUCCESS('Default data created successfully!'))
