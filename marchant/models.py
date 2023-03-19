from django.db import models

# Create your models here.

CATEGORIES = (
    ('H', 'House'),
    ('A', 'Apartment'),
    ('O', 'Office'),
    ('R', 'Room'),
)

TIMEFRAME = (
    ('L', 'Lifetime'),
    ('M', 'Monthly'),
    ('Y', 'Yearly')
)

class Product(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORIES, max_length=1, default='R')
    timeframe = models.CharField(choices=TIMEFRAME, max_length=1, default='Y')
    size = models.CharField(max_length=30)
    # sub_product = models.ManyToManyField('SubProduct', blank=True)
    value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    images = models.ForeignKey('Images', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE, blank=False, null=True)
    # review = models.ManyToManyField('Reviews', blank=True)
    
    @property
    def rate(self):
        ratex = self.rating
        summ = ratex.rate1+ratex.rate2*2+ratex.rate3*3+ratex.rate4*4+ratex.rate5*5
        sumz = ratex.rate1+ratex.rate2+ratex.rate3+ratex.rate4+ratex.rate5
        rates = summ/sumz
        return round(rates,2)

    def __str__(self) -> str:
        return self.title

class Rating(models.Model):
    """
    Rating System on a Scale of (5)
    """
    rate1 = models.IntegerField(default=1)
    rate2 = models.IntegerField(default=1)
    rate3 = models.IntegerField(default=1)
    rate4 = models.IntegerField(default=1)
    rate5 = models.IntegerField(default=1)
    

class Images(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)

class Review(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
    reply = models.ForeignKey('ReviewReply', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def rate(self):
        rate = 1 
        if self.rating.rate1>rate:
            rate = self.rating.rate1
        elif self.rating.rate2>rate:
            rate = self.rating.rate2
        elif self.rating.rate3>rate:
            rate = self.rating.rate3
        elif self.rating.rate4>rate:
            rate = self.rating.rate4
        elif self.rating.rate5>rate:
            rate = self.rating.rate5
        return rate

class ReviewReply(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
