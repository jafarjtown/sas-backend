from django.db import models
from datetime import timedelta 
# Create your models here.

class House(models.Model):
    address = models.TextField()
    no_of_rooms = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    merchant = models.ForeignKey('authentication.User', related_name='houses', null=True, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='houses', null=True, on_delete=models.SET_NULL)
    images = models.ManyToManyField('Image', related_name='house', blank=True)
    active = models.BooleanField(default=False)
    coupon =models.CharField(max_length=25,blank=True)
    
    
    def is_booked(self):
        return True if hasattr(self, 'booked') else False
    
    @property
    def cat_name(self):
        return self.category.name
    
    @property
    def merchant_name(self):
        return self.merchant.username

class Image(models.Model):
    file = models.ImageField(upload_to='images/houses')
    address = models.TextField()


class Booked(models.Model):
    customer = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='booked')
    house = models.OneToOneField('House', related_name='booked', on_delete=models.CASCADE)
    at_price = models.FloatField(default=0.0)
    coupon = models.ForeignKey('Coupon', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey('Payment', null=True, on_delete=models.SET_NULL)
    
class Payment(models.Model):
    user_id = models.CharField(max_length=25)
    ref_id = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateField(auto_now_add=True)
    verify = models.BooleanField(default=False)
    
class Category(models.Model):
    name = models.CharField(max_length=25)    
    
class Coupon(models.Model):
    code = models.CharField(max_length=15, null=True)
    percentage = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=15, blank=True)