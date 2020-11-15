from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"Account is created for " + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username Or Password is incorrect")
                

    context = {}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customer = Customer.objects.all()
    order = Orders.objects.all()

    total_orders = order.count()
    total_delivered = order.filter(status='Delivered').count()
    total_pending = order.filter(status='Pending').count()

    context = { 'customer': customer,'order':order, 'total_orders': total_orders, 'total_delivered':total_delivered,'total_pending':total_pending }


    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.orders_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

    products = Products.objects.all()

    return render(request, 'accounts/products.html', {'products': products} )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.orders_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,'orders': orders,'myFilter':myFilter}

    return render(request, 'accounts/customer.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk_del):

    order = Orders.objects.get(id=pk_del)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request,'accounts/delete.html',context)