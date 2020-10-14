from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def home(request):
    customer = Customer.objects.all()
    order = Orders.objects.all()

    total_orders = order.count()
    total_delivered = order.filter(status='Delivered').count()
    total_pending = order.filter(status='Pending').count()

    context = { 'customer': customer,'order':order, 'total_orders': total_orders, 'total_delivered':total_delivered,'total_pending':total_pending }


    return render(request, 'accounts/dashboard.html', context)

    
def products(request):

    products = Products.objects.all()

    return render(request, 'accounts/products.html', {'products': products} )


def customer(request):
    return render(request, 'accounts/customer.html')