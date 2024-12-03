# myapp/views.py
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product, Service, VideoSection, FunFact


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