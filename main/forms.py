# main/forms.py
from django import forms
from .models import ContactSubmission, NewsletterSubscription

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['full_name', 'email', 'organization', 'event_type', 'event_details']
        widgets = {
            'event_details': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'event_details':
                field.widget.attrs.update({'class': 'form-control'})

class NewsletterForm(forms.ModelForm):
    agree = forms.BooleanField(required=True, label='I agree to receive monthly newsletters and updates from Fusion Force LLC')
    
    class Meta:
        model = NewsletterSubscription
        fields = ['name', 'email', 'source']
        widgets = {
            'source': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Email', 'required': True})
        self.fields['agree'].widget.attrs.update({'class': 'form-check-input', 'required': True})
