# context_processors.py

from .models import *
from django.templatetags.static import static


def contact_info(request):
    contact = ContactInfo.objects.first()
    social_links = SocialMedia.objects.all()
    return {
        'contact_info': contact,
        'social_links': social_links
    }


def site_logo(request):
    logo = SiteLogo.objects.first()  # Assuming you only have one logo
    return {
        'site_logo': logo
    }



def banners(request):
    # Get the banners from the database
    banners = Banner.objects.all()

    # If no banners in the database, use default banners
    if not banners.exists():
        banners = [
            {
                'heading': 'Beautiful Living Room Decor Ideas',
                'subheading': 'Modern Home, USA',
                'image': static('assets/images/deal-01.jpg')
            },
            {
                'heading': 'Creative Bedroom Designs',
                'subheading': 'Luxury Apartments, Australia',
                'image': static('assets/images/banner-02.jpg')
            },
            {
                'heading': 'Elegant Dining Space Inspirations',
                'subheading': 'Miami, South Florida',
                'image': static('assets/images/banner-03.jpg')
            },
        ]
    return {
        'banners': banners
    }

def services_context(request):
    services = Service.objects.prefetch_related('options').all()
    return {
        'services': services,
    }

# myapp/context_processors.py

def fun_facts_and_video_context(request):
    # Get the most recent FunFact object from the database
    fun_facts = FunFact.objects.first()

    if fun_facts:
        context = {
            'video_url': fun_facts.video_url,  # Dynamic video URL from the database
            'fun_facts': {
                'properties_sold': fun_facts.properties_sold,
                'years_experience': fun_facts.years_experience,
                'satisfied_clients': fun_facts.satisfied_clients
            }
        }
    else:
        # Default context if no FunFact is available in the database
        context = {
            'video_url': 'https://youtube.com/your-property-tour-video',
            'fun_facts': {
                'properties_sold': 0,
                'years_experience': 0,
                'satisfied_clients': 0
            }
        }
    return context
