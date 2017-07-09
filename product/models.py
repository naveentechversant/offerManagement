from django.db import models

# Create your models here.
"""
Product Master
"""
class Product(models.Model):
	code = models.CharField(max_length=100)
	name = models.CharField(max_length=300)
	stock = models.IntegerField()
	created_date = models.DateTimeField(auto_now_add=True)
	price = models.DecimalField(decimal_places=2, max_digits=12, default=0.0)

	def __unicode__(self):
	    return self.code



class Offers(models.Model):
	code = models.CharField(max_length=100)
	start = models.DateTimeField()
	end = models.DateTimeField()
	discount = models.DecimalField(decimal_places=2, max_digits=12, default=0.0)
	type_of_discount = models.CharField(max_length=25) # A - > Absolute amount P-> Percentage
	def __unicode__(self):
	    return self.code