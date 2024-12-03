# models.py
from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.core.exceptions import ValidationError


class ContactInfo(models.Model):
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class SocialMedia(models.Model):
    FACEBOOK = 'facebook'
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'
    LINKEDIN = 'linkedin'
    YOUTUBE = 'youtube'

    PLATFORM_CHOICES = [
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (INSTAGRAM, 'Instagram'),
        (LINKEDIN, 'LinkedIn'),
        (YOUTUBE, 'YouTube'),
    ]

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        default=FACEBOOK
    )
    url = models.URLField(max_length=255)

    def __str__(self):
        return f'{self.get_platform_display()} - {self.url}'



class SiteLogo(models.Model):
    logo = models.ImageField(
        upload_to='logos/',
        help_text="Upload a logo with a rendered size of 212x50 px, aspect ratio of 106:25. The intrinsic size should be 1025x243 px."
    )
    
    def __str__(self):
        return "Site Logo"



class Banner(models.Model):
    heading = models.CharField(max_length=255, help_text="Main heading text for the banner.")
    subheading = models.CharField(max_length=255, help_text="Subheading or location for the banner.")
    image = models.ImageField(upload_to='banners/', help_text="Upload an image with rendered size 520x395 px, aspect ratio 104:79.")
    
    def __str__(self):
        return f"Banner: {self.heading}"
    

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100)  # FontAwesome icon class name
    image = models.ImageField(upload_to='services/')          
    order = models.PositiveIntegerField(default=0)  # For ordering the services in display

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ServiceOption(models.Model):
    service = models.ForeignKey(Service, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.service.name})"


class Product(models.Model):
    service_option = models.ForeignKey(ServiceOption, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255,default="short description", blank=True, null=True, help_text="Short description for product cards")
    description = models.TextField(blank=True, null=True,default="long description", help_text="Detailed description for product detail page")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.FloatField(default=0)
    emi_starts_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_new = models.BooleanField(default=False)
    made_to_order = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields
    dimensions = models.CharField(max_length=255, blank=True, null=True, help_text="Product dimensions (e.g., LxWxH)")
    maintenance = models.TextField(blank=True, null=True, help_text="Maintenance guidelines for the product")
    warranty_summary = models.TextField(blank=True, null=True, help_text="Warranty details for the product")
    return_policy = models.TextField(blank=True, null=True, help_text="Return policy for the product")

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    def discounted_price(self):
        """
        Returns the price after applying the discount.
        """
        # Convert discount to a Decimal
        discount_decimal = Decimal(self.discount) / Decimal(100)
        return self.price * (Decimal(1) - discount_decimal)

    def __str__(self):
        return f"{self.name} (Service Option: {self.service_option.name})"
    
    @property
    def discounted_price(self):
        if self.discount_percentage and self.original_price:
            return self.original_price * (1 - (self.discount_percentage / 100))
        return self.price


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Feature name (e.g., Key Feature)")
    value = models.TextField(blank=True, null=True, help_text="Details or description of the feature")

    def __str__(self):
        return f"{self.name} ({self.product.name})"


class CustomizationOption(models.Model):
    product = models.ForeignKey(Product, related_name='customizations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Name of the customization option (e.g., Polish Finish, Size)")
    choices = models.JSONField(default=dict, help_text="Choices for customization as a JSON object (e.g., {'Queen': 100, 'King': 150})")

    def __str__(self):
        return f"{self.name} ({self.product.name})"

class VideoSection(models.Model):
    title = models.CharField(max_length=255, help_text="Main title of the video section")
    subtitle = models.CharField(max_length=255, help_text="Subtitle or tagline of the video section")
    video_thumbnail = models.ImageField(upload_to="videos/", help_text="Thumbnail image for the video")
    video_url = models.URLField(blank=True, null=True, help_text="URL of the video (e.g., YouTube link)")
    video_file = models.FileField(upload_to="videos/", blank=True, null=True, help_text="Upload a video file")

    def __str__(self):
        return self.title

    def clean(self):
        """
        Ensure that either video_url or video_file is provided, but not both.
        """
        if self.video_url and self.video_file:
            raise ValidationError("You can only provide a video URL or upload a video file, not both.")
        if not self.video_url and not self.video_file:
            raise ValidationError("You must provide either a video URL or upload a video file.")
    
class FunFact(models.Model):
    title = models.CharField(max_length=255, help_text="Title for the fun fact (e.g., 'Properties Sold')")
    value = models.PositiveIntegerField(help_text="Numerical value for the fun fact (e.g., 34)")
    description = models.CharField(max_length=255, help_text="Short description (e.g., 'Finished Now')")

    def __str__(self):
        return self.title
