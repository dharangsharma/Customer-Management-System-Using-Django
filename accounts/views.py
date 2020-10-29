from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter 

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


def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.orders_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,'orders': orders,'myFilter':myFilter}

    return render(request, 'accounts/customer.html', context )

def createOrder(request,pk_test):

    OrderFormSet = inlineformset_factory(Customer,Orders,fields=('product','status'),extra=5)  #Customer = parent model,Orders = child model
    customer = Customer.objects.get(id=pk_test)
    formset = OrderFormSet(queryset=Orders.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        # print("print post", request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk_test):

    order = Orders.objects.get(id=pk_test)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk_del):

    order = Orders.objects.get(id=pk_del)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request,'accounts/delete.html',context)