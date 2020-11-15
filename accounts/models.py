from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    CATAGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
                )
    name = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=200,null=True,choices=CATAGORY)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


    
class Orders(models.Model):
    STATUS = (
        ('pending','pending'),
        ('out for delivery','out for delivery'),
        ('delivered','delivered'),
             )
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)

    def __str__(self):
        return self.product.name

    



