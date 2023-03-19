from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

SPECIALIZATION = (
    ('R', 'Rent'),
    ('S', 'Sell'),
    ('B', 'Sell & Rent'),
    ('C', 'Customer')
)

class User(AbstractUser):
    phone_no = models.CharField(max_length=11)
    second_phone_no = models.CharField(max_length=11)
    nationality = models.CharField(max_length=20)
    state_of_resident = models.CharField(max_length=25)
    local_govt = models.CharField(max_length=25)
    business_state = models.CharField(max_length=25)
    specialization = models.CharField(choices=SPECIALIZATION, max_length=1, default='C')
    is_merchant = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)