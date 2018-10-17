from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
# from stockmarket.forms import LoginForm
from .models import CustomUser, Stock, Order
import requests
import json
import pdb
from .forms import StockForm
# Create your views here.


def successful_login(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    orders = user.orders.all()
    form = StockForm()
    return render(request, '../templates/stock_portfolio.html',{'user':user, 'orders': orders, 'form': form})

def signup(request):
    err=0
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        c_password = request.POST.get("confirm_password")
        #pdb.set_trace()
        if password == c_password:
            user = CustomUser()
            user.username = username
            user.set_password(password)
            user.save()
            return render(request,'../templates/stock_portfolio.html',{'user':user})
        else:
            err=1
            return render(request,'../templates/signup.html',{'err':err})
    return render(request,'../templates/signup.html')
def loginview(request):
    err=0
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        #pdb.set_trace()
        if user is not None:
            login(request, user)
            pk = user.id
            return redirect('successful_login', pk=pk)
        else:
            err=1
            return render(request,'../templates/login.html',{'response':err})

    return render(request, '../templates/login.html')


def logoutview(request):
    logout(request)
    return render(request,'../templates/login.html')

@login_required(login_url='login')
def buy(request, pk, sn):
    err=""
    if request.method=="POST":
        user = get_object_or_404(CustomUser, pk=pk)
        stock = get_object_or_404(Stock, name=sn)
        quantity = float(request.POST.get("quantity-"+sn))
        if quantity<0:
            err="Quantity can't be negative!"
            return render(request,'../templates/stock_portfolio.html',{'user':user,'err':err})
        else:
            if stock.ltp*quantity>user.total_fund:
                err="You don't have this much fund!"
                return render(request, '../templates/stock_portfolio.html', {'user': user,'err':err})
            order = Order(trader=user, stock=stock, order_type="BUY", quantity=quantity)
            order.save()
            user.total_fund-=order.amount
            user.save()
            orders = user.orders.all()
            return render(request, '../templates/stock_portfolio.html', {'user': user, 'orders': orders})

    else:
        user = get_object_or_404(CustomUser, pk=pk)
        render(request, '../templates/stock_portfolio.html', {'user': user})
@login_required
def sell(request, pk, sn):
    err=""
    if request.method=="POST":
        user = get_object_or_404(CustomUser, pk=pk)
        stock = get_object_or_404(Stock, name=sn)
        quantity = float(request.POST.get("quantity-"+sn))
        if quantity>0:
            order = Order(trader=user, stock=stock, _type="SELL", quantity=quantity)
            order.save()
            user.total_fund+=order.amount
            user.save()
            orders = user.orders.all()
            return render(request, '../templates/stock_portfolio.html', {'user': user, 'orders': orders})
        else:
            err=" Quantity can't be negative!"
            return render(request, '../templates/stock_portfolio.html', {'user': user,'err':err})
        #pdb.set_trace()
    else:
        user = get_object_or_404(CustomUser, pk=pk)
        return render(request, '../templates/stock_portfolio.html', {'user': user})


from dal import autocomplete

class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Stock.objects.none()

        qs = Stock.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs