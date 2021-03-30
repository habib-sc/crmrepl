from django.shortcuts import render, redirect
from django.http import HttpResponse

from datetime import datetime

from django.forms import inlineformset_factory
from .forms import OrderForm, UserRegisterForm, CustomerForm

from .models import *

from .filters import orderFilter

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages

from .decorators import unauthenticated_user_only, allowed_users_only, admin_only


# Register views
#=============================================================
@unauthenticated_user_only
def registerUser(request):  
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for '+ username)

            return redirect('login')

    context ={
        'form': form,
    }

    return render(request, 'register.html', context) 


    

# Login views
#=============================================================
@unauthenticated_user_only
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password Incorrect!')
            return render(request, 'login.html') 
                
    return render(request, 'login.html') 


# LogOut views
#=============================================================
def logoutUser(request):
    logout(request)
    return redirect('login')


# User Page views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders, 'total_orders': total_orders, 'total_delivered': total_delivered,
        'total_pending': total_pending, 
    }

    return render(request, 'user.html', context)



# Home views
#=============================================================
@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()

    context = {'customers': customers, 'orders': orders, 'total_customers': total_customers,
    'total_orders': total_orders, 'total_delivered': total_delivered,
    'total_pending': total_pending,
    }

    return render(request, 'dashboard.html', context)

# Products views
#=============================================================
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


# Customers views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = orderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'myFilter': myFilter}
    return render(request, 'customers.html', context)


# Add Customers views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def addCustomer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        new_customer = Customer(name=name, phone=phone, email=email, created_date=datetime.today())
        new_customer.save()
        return redirect('/')

    return render(request, 'add_customer.html')


# Delete Customers views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    
    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'delete_customer.html', context)


# Customers Profile setting
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Customer'])
def profileSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    
    return render(request, 'profile_setting.html', context)




# Create Order views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'order.html', context)


# Place Order form Customer Profile
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def placeOrderCus(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}

    return render(request, 'order_set.html', context)


# Update Order views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'order.html', context)


# Delete Order views
#=============================================================
@login_required(login_url='login')
@allowed_users_only(allowed_roles=['Admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'delete_order.html', context)