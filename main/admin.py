# admin.py - COMPLETE VERSION WITH FUSION-FORCE BRANDING
'''
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import (
     AboutContent, Service, NewsletterContent,
    Testimonial, Event, GalleryImage, ContactSubmission,
    NewsletterSubscription, SystemLog
)

# ============ CUSTOM ADMIN SITE ============
class FusionForceAdminSite(admin.AdminSite):
    site_header = "FUSION-FORCE ADMIN"
    site_title = "Fusion Force Administration"
    index_title = "Dashboard"
    
    def get_app_list(self, request, app_label=None):
        """
        Customize the app list to group related models
        """
        app_list = super().get_app_list(request, app_label)
        
        # Custom grouping for Fusion Force
        for app in app_list:
            if app['app_label'] == 'main':  # Your app name
                # Group content management
                content_models = [ 'AboutContent', 'NewsletterContent']
                form_models = ['ContactSubmission', 'NewsletterSubscription']
                display_models = ['Service', 'Testimonial', 'Event', 'GalleryImage']
                system_models = ['SystemLog']
                
                content_list = []
                form_list = []
                display_list = []
                system_list = []
                
                for model in app['models']:
                    if model['object_name'] in content_models:
                        content_list.append(model)
                    elif model['object_name'] in form_models:
                        form_list.append(model)
                    elif model['object_name'] in display_models:
                        display_list.append(model)
                    elif model['object_name'] in system_models:
                        system_list.append(model)
                
                # Reorganize with custom sections
                app['models'] = content_list + display_list + form_list + system_list
        
        return app_list

# Create custom admin site instance
admin_site = FusionForceAdminSite(name='fusionforce_admin')

# ============ ADMIN CLASSES ============

@admin.register(AboutContent, site=admin_site)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'image')
        }),
        ('Bullet Points', {
            'fields': ('bullet_points',),
            'description': 'Enter each bullet point on a new line'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'topic_count', 'created_at']
    list_filter = ['service_type']
    search_fields = ['title', 'description', 'topics']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Service Info', {
            'fields': ('title', 'service_type', 'description')
        }),
        ('Display', {
            'fields': ('icon_class', 'topics')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def topic_count(self, obj):
        if obj.topics:
            return len(obj.topics.split(','))
        return 0
    topic_count.short_description = 'Topics'

@admin.register(Testimonial, site=admin_site)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'position', 'is_active', 'created_at', 'avatar_preview']
    list_filter = ['is_active', 'company']
    list_editable = ['is_active']
    search_fields = ['client_name', 'company', 'position', 'content']
    readonly_fields = ['created_at', 'updated_at', 'avatar_preview']
    
    fieldsets = (
        ('Client Info', {
            'fields': ('client_name', 'position', 'company')
        }),
        ('Testimonial', {
            'fields': ('content', 'avatar')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.avatar.url)
        return "No Image"
    avatar_preview.short_description = 'Preview'

@admin.register(Event, site=admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'created_at']
    list_filter = ['event_type']
    search_fields = ['title', 'description', 'event_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Info', {
            'fields': ('title', 'event_type', 'description')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NewsletterContent, site=admin_site)
class NewsletterContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subscriber_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at', 'subscriber_count')
    
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'subtitle', 'image', 'form_title', 'form_description')
        }),
        ('Benefits', {
            'fields': ('benefits',),
            'description': 'Add each benefit on a new line. They will be displayed in two columns.'
        }),
        ('Statistics', {
            'fields': ('subscriber_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subscriber_count(self, obj):
        return NewsletterSubscription.objects.count()
    subscriber_count.short_description = 'Total Subscribers'

@admin.register(GalleryImage, site=admin_site)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'display_order', 'is_active', 'created_at', 'image_preview')
    list_filter = ('event_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'image', 'event_type', 'description')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(ContactSubmission, site=admin_site)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'organization', 'event_type', 'status', 'submitted_at', 'contacted_status')
    list_filter = ('status', 'event_type', 'submitted_at')
    search_fields = ('full_name', 'email', 'organization', 'event_details')
    list_editable = ('status',)
    readonly_fields = ('submitted_at', 'contacted_at', 'user_info')
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'organization')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_details')
        }),
        ('Status & Follow-up', {
            'fields': ('status', 'contacted_at', 'notes')
        }),
        ('System Information', {
            'fields': ('submitted_at', 'user_info'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_contacted', 'mark_as_booked']
    
    def contacted_status(self, obj):
        if obj.contacted_at:
            return format_html(
                '<span style="color: green;">✓ Contacted</span><br><small>{}</small>',
                obj.contacted_at.strftime('%Y-%m-%d %H:%M')
            )
        return format_html('<span style="color: orange;">Pending</span>')
    contacted_status.short_description = 'Contact Status'
    
    def user_info(self, obj):
        return format_html(
            'Submitted: {}<br>Last updated: {}',
            obj.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            obj.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        )
    user_info.short_description = 'Submission Details'
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='contacted', contacted_at=timezone.now())
        self.message_user(request, f'{updated} submission(s) marked as contacted.')
    mark_as_contacted.short_description = "Mark selected as contacted"
    
    def mark_as_booked(self, request, queryset):
        updated = queryset.update(status='booked')
        self.message_user(request, f'{updated} submission(s) marked as booked.')
    mark_as_booked.short_description = "Mark selected as booked"

@admin.register(NewsletterSubscription, site=admin_site)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'source', 'is_active', 'subscribed_at', 'days_since_subscription')
    list_filter = ('source', 'is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    list_editable = ('is_active',)
    readonly_fields = ('subscribed_at', 'last_email_sent')
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('name', 'email', 'source', 'agreed_to_terms')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'last_email_sent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_emails', 'deactivate_subscriptions']
    
    def days_since_subscription(self, obj):
        delta = timezone.now() - obj.subscribed_at
        return delta.days
    days_since_subscription.short_description = 'Days Subscribed'
    
    def export_emails(self, request, queryset):
        emails = "\n".join([sub.email for sub in queryset])
        self.message_user(request, f"Copied {queryset.count()} emails to clipboard.")
        return emails
    export_emails.short_description = "Export selected emails"
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscription(s) deactivated.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

@admin.register(SystemLog, site=admin_site)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('log_level_display', 'message_short', 'source', 'created_at', 'user_ip')
    list_filter = ('log_level', 'source', 'created_at')
    search_fields = ('message', 'source', 'user_ip')
    readonly_fields = ('created_at', 'user_ip', 'user_agent')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Log Details', {
            'fields': ('log_level', 'message', 'source')
        }),
        ('User Information', {
            'fields': ('user_ip', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['clear_old_logs']
    
    def log_level_display(self, obj):
        colors = {
            'info': 'blue',
            'warning': 'orange',
            'error': 'red',
            'success': 'green'
        }
        color = colors.get(obj.log_level, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_log_level_display()
        )
    log_level_display.short_description = 'Level'
    
    def message_short(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_short.short_description = 'Message'
    
    def clear_old_logs(self, request, queryset):
        # Keep logs from last 30 days
        cutoff_date = timezone.now() - timedelta(days=30)
        old_logs = SystemLog.objects.filter(created_at__lt=cutoff_date)
        count = old_logs.count()
        old_logs.delete()
        self.message_user(request, f'Deleted {count} logs older than 30 days.')
    clear_old_logs.short_description = "Clear logs older than 30 days"

# ============ REGISTER DEFAULT ADMIN ============
# Replace default admin site with custom one
from django.contrib.admin.sites import site as default_site
default_site.__class__ = FusionForceAdminSite

'''