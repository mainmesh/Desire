#from distutils.command.upload import upload
from itertools import product
from multiprocessing.spawn import old_main_modules
from statistics import quantiles
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.core.validators import MaxLengthValidator, MinValueValidator


STATE_CHOICE = (
    ('Mombasa', 'Mombasa'),
    ('Kwale', 'Kwale'),
    ('Kilifi', 'Kilifi'),
    ('Tana River', 'Tana River'),
    ('Lamu', 'Lamu'),
    ('Taita–Taveta', 'Taita–Taveta'),
    ('Garissa', 'Garissa'),
    ('Wajir', 'Wajir'),
    ('Mandera', 'Mandera'),
    ('Marsabit', 'Marsabit'),
    ('Isiolo', 'Isiolo'),
    ('Meru', 'Meru'),
    ('Tharaka-Nithi', 'Tharaka-Nithi'),
    ('Embu', 'Embu'),
    ('Kitui', 'Kitui'),
    ('Machakos', 'Machakos'),
    ('Makueni', 'Makueni'),
    ('Nyandarua', 'Nyandarua'),
    ('Nyeri', 'Nyeri'),
    ('Kirinyaga', 'Kirinyaga'),
    ('Murang’a', 'Murang’a'),
    ('Kiambu', 'Kiambu'),
    ('Turkana', 'Turkana'),
    ('West Pokot', 'West Pokot'),
    ('Samburu', 'Samburu'),
    ('Trans-Nzoia', 'Trans-Nzoia'),
    ('Uasin Gishu', 'Uasin Gishu'),
    ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
    ('Nandi', 'Nandi'),
    ('Baringo', 'Baringo'),
    ('Laikipia', 'Laikipia'),
    ('Nakuru', 'Nakuru'),
    ('Narok', 'Narok'),
    ('Kajiado', 'Kajiado'),
    ('Kericho', 'Kericho'),
    ('Bomet', 'Bomet'),
    ('Kakamega', 'Kakamega'),
    ('Vihiga', 'Vihiga'),
    ('Bungoma', 'Bungoma'),
    ('Busia', 'Busia'),
    ('Siaya', 'Siaya'),
    ('Kisumu', 'Kisumu'),
    ('Homa Bay', 'Homa Bay'),
    ('Migori', 'Migori'),
    ('Kisii', 'Kisii'),
    ('Nyamira', 'Nyamira'),
    ('Nairobi City', 'Nairobi City'),
)


class Customer(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=90)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE, max_length=80)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('Pills', 'Pills'),
    ('Sex Toys', 'Sex Toys'),
    ('ElectronicAccessories', 'Electronic Accessories'),
    # ('BW', 'Bottom Wear'),
)

class Brand(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    def __str__(self):
        return (self.name)
    
# class Category(models.Model):
#     category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
    
#     def __str__(self):
#         return (self.category)

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discounted_prie = models.FloatField()
    short_description = HTMLField(max_length=110)
    description = HTMLField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
    product_image = models.ImageField(upload_to='productimg', null=False , blank=False)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def totalCost(self):
        return self.quantity * self.product.discounted_prie


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=60, choices=STATUS_CHOICES, default='Pending')

    @property
    def totalCost(self):
        return self.quantity * self.product.discounted_prie


# Create your models here.
class Verification(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=150)
	verify = models.BooleanField(default=False)
    