# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    HomeContent, AboutContent, Service, NewsletterContent, 
    Testimonial, Event, GalleryImage, ContactSubmission, 
    NewsletterSubscription, SystemLog
)

# ============ CUSTOM ADMIN SITE CONFIG ============
admin.site.site_header = "FUSION-FORCE ADMIN"
admin.site.site_title = "Fusion Force Administration"
admin.site.index_title = "Dashboard"

# ============ CUSTOM ADMIN CLASSES ============
@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'hero_image')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AboutContent)
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

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'created_at']
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

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'position', 'is_active', 'created_at']
    list_filter = ['is_active', 'company']
    list_editable = ['is_active']
    search_fields = ['client_name', 'company', 'position', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
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

@admin.register(Event)
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

@admin.register(NewsletterContent)
class NewsletterContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'subtitle', 'image', 'form_title', 'form_description')
        }),
        ('Benefits', {
            'fields': ('benefits',),
            'description': 'Add each benefit on a new line. They will be displayed in two columns.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'display_order', 'is_active', 'created_at')
    list_filter = ('event_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
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

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'organization', 'event_type', 'status', 'submitted_at')
    list_filter = ('status', 'event_type', 'submitted_at')
    search_fields = ('full_name', 'email', 'organization', 'event_details')
    list_editable = ('status',)
    readonly_fields = ('submitted_at', 'contacted_at')
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
    )

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'source', 'is_active', 'subscribed_at')
    list_filter = ('source', 'is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    list_editable = ('is_active',)
    readonly_fields = ('subscribed_at', 'last_email_sent')
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('name', 'email', 'source')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'last_email_sent'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('log_level', 'message_short', 'source', 'created_at')
    list_filter = ('log_level', 'source', 'created_at')
    search_fields = ('message', 'source')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Log Details', {
            'fields': ('log_level', 'message', 'source')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def message_short(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_short.short_description = 'Message'