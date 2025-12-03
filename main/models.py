# models.py - NO CIRCULAR IMPORTS!
# main/models.py - COMMENT OUT FOR NOW
'''
from django.db import models

class AboutContent(models.Model):
    title = models.CharField(max_length=200, default="Pamela Robinson")
    description = models.TextField(default="Pamela Robinson is a keynote speaker, corporate and leadership trainer, founder of Fusion Force and a recognized expert in sales and marketing support for hospitality companies.")
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    bullet_points = models.TextField(
        default="Keynote Speaker\nLeadership Trainer\nHospitality Expert\nGlobal Experience",
        help_text="Enter each bullet point on a new line"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Service(models.Model):
    SERVICE_TYPES = [
        ('keynote', 'Keynote Speaking'),
        ('training', 'Corporate Training'),
        ('consulting', 'Strategic Consulting'),
    ]
    
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, help_text="Font Awesome icon class (e.g., fas fa-microphone)")
    topics = models.TextField(help_text="Enter topics separated by commas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    content = models.TextField()
    avatar = models.ImageField(upload_to='testimonial_avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.client_name} - {self.company}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    event_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class NewsletterContent(models.Model):
    title = models.CharField(max_length=200, default="Monthly Newsletter")
    subtitle = models.CharField(max_length=300, default="Get exclusive insights and industry updates delivered to your inbox")
    image = models.ImageField(upload_to='newsletter/', null=True, blank=True, help_text="Newsletter cover image")
    benefits = models.TextField(default="Leadership Strategies\nIndustry Updates\nCase Studies\nEvent Announcements\nExclusive Content\nSuccess Stories", help_text="Add each benefit on a new line")
    form_title = models.CharField(max_length=200, default="Join Our Community")
    form_description = models.TextField(default="Get exclusive leadership insights, industry trends, and event updates delivered directly to your inbox each month.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Newsletter Content"
        verbose_name_plural = "Newsletter Content"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Newsletter Content - {self.updated_at.strftime('%Y-%m-%d')}"

class GalleryImage(models.Model):
    EVENT_TYPE_CHOICES = [
        ('corporate', 'Corporate Leadership'),
        ('empowerment', 'Women Empowerment'),
        ('hospitality', 'Hospitality Awards'),
        ('latest', 'Latest Event'),
        ('keynote', 'Keynote Speaking'),
        ('training', 'Corporate Training'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='corporate')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Higher number appears first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['-display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_event_type_display()}"

# ============ FORM SUBMISSION MODELS ============

class ContactSubmission(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    organization = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    event_details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(auto_now_add=True)
    contacted_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.organization}"

class NewsletterSubscription(models.Model):
    SOURCE_CHOICES = [
        ('newsletter_section', 'Newsletter Section'),
        ('footer', 'Website Footer'),
    ]
    
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='newsletter_section')
    agreed_to_terms = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_email_sent = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return f"{self.email}"

class SystemLog(models.Model):
    LOG_LEVELS = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    ]
    
    log_level = models.CharField(max_length=20, choices=LOG_LEVELS, default='info')
    message = models.TextField()
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "System Log"
        verbose_name_plural = "System Logs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_log_level_display()} - {self.message[:50]}"

'''        