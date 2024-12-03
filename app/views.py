# myapp/views.py
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product, Service, VideoSection, FunFact

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages


def index(request):
    video_section = VideoSection.objects.first()
    fun_facts = FunFact.objects.all()
    latest_products = Product.objects.filter(in_stock=True).order_by('-created_at')[:5]
    return render(request, 'myapp/index.html', {"video_section": video_section, "fun_facts": fun_facts,"latest_products": latest_products})


def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'myapp/service_detail.html', {'service': service})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


from .models import Product

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'myapp/product_detail.html', {'product': product})


from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone_number = request.POST.get('Ph')

        # Construct the email message
        email_message = f"Name: {name}\nPhone number : {phone_number} \nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send email
            send_mail(
                subject=subject,
                message=email_message,
                from_email='info@cmhomedecor.in',  # Your email address
                recipient_list=['info@cmhomedecor.in'],  # Where to send
                fail_silently=False,
            )
            return render(request, 'myapp/Success.html')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'myapp/index.html')
