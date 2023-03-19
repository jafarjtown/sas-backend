from django.contrib import admin
from .models import Coupon,House,Booked,Payment
# Register your models here.

admin.site.register(Coupon)
admin.site.register(House)
admin.site.register(Booked)
admin.site.register(Payment)