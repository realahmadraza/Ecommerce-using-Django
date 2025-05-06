from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Collection(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    images = models.ImageField(upload_to='images/products', blank=False, null=False, default='images/products/default image.jpg')
    quantity = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True, null=True)
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse("productdetail", kwargs={"pk": self.pk, "slug": self.slug})
    
    def __str__(self):
        return self.name

class ProductInstruction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    careinstructions = models.CharField(max_length=40, blank=False, null=False)
    Fittype =  models.CharField(max_length=40, blank=False, null=False)
    color =  models.CharField(max_length=40, blank=False, null=False)
    cloth =  models.CharField(max_length=40, blank=False, null=False)
    sleeves =  models.CharField(max_length=40, blank=False, null=False)
    design =  models.CharField(max_length=40, blank=False, null=False)
    wash =  models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return 'Type Product Instructions Here'

class Category(models.Model):
    Category = models.CharField(max_length=255, unique=True, blank=False)
    Quantity = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['Category']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.Category

class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sales = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ['-sales']
        verbose_name_plural = 'Sales'

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Ordered - {self.product.name} \n | Quantity - {self.quantity}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart - {self.created_at}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1, "Quantity cannot be less than 1"), MaxValueValidator(10, "Quantity cannot be more than 10")], default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        unique_together = ['cart', 'product']
        verbose_name_plural = 'CartItems'
    
    def __str__(self):
        return f'CartItem - {self.product.name} \n Quantity - {self.quantity}'

class SearchedQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    search_query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Searched Query'
        verbose_name_plural = 'Searched Queries'
    def __str__(self):
        return f'Searched Quereis by {self.user}'

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, default='User"s name', blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    locality = models.CharField(max_length=40, default=False, blank=False, null=False)
    landmark = models.CharField(max_length=50, default=False , blank=False, null=False)
    phone = PhoneNumberField(region='IN', default='region')
    alternate_phone = PhoneNumberField(region='IN', default='region')
    state = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    pin = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.user}'s address"
    
class About(models.Model):
    allabout = models.TextField(blank=False, null=False)
    mainimage = models.ImageField(upload_to='images/maincentre', blank=False, null=True)
    
    centre1city = models.CharField(max_length=40, default='Mumbai', blank=False, null=False)
    centre1info = models.TextField(blank=False, null=False)
    centre1image = models.ImageField(upload_to='images/centre1', blank=False, null=True)

    centre2city = models.CharField(max_length=40, default='Kolakata', blank=False, null=False)
    centre2info = models.TextField(blank=False, null=False)
    centre2image = models.ImageField(upload_to='images/centre2', blank=False, null=True)

    centre3city = models.CharField(max_length=40, default='Banglore', blank=False, null=False)
    centre3info = models.TextField(blank=False, null=False)
    centre3image = models.ImageField(upload_to='images/centre3', blank=False, null=True)

    def __str__(self):
        return 'About Us'
    
    class Meta:
        verbose_name_plural = 'About Us'

class Footerinfo(models.Model): 
    short_About = models.CharField(max_length=265, blank=False, null=False)
    City = models.CharField(max_length=40, blank=False, null=False)
    email = models.EmailField(max_length=40, blank=False, null=False)
    phone = PhoneNumberField(region='IN', default='region')
    telephone = PhoneNumberField(region='IN', default='region')

    def __str__(self):
        return 'Footer Information'
    
    class Meta:
        verbose_name_plural = 'Footer Informations'