# fusion_force/urls.py
from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/submit/', views.newsletter_submit, name='newsletter_submit'),
    
    # REMOVE admin URLs:
    # path('admin/', admin.site.urls),
]

# Remove this if you have it:
# handler404 = 'main.views.custom_404'