from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
# from stockmarket.forms import LoginForm
from .models import CustomUser,Stock
import requests
import json
import pdb
# Create your views here.
def get_stock_price(stock_name):
    url = "http://finance.google.com/finance/info?client=ig&q=NSE:"+stock_name.upper()
    stock_data = requests.get(url)
    stock_data = stock_data.content.decode('utf-8').replace("\n","").replace("/","")
    stock_json = json.loads(stock_data)[0]
    price = float(stock_json['l'].replace(",",""))
    return price


def successful_login(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    allstocks = user.stocks.all()
    for stock in allstocks:
        stock.current_price = get_stock_price(str(stock.stock_name))
        stock.save()
    user.save()
    return render(request, '../templates/stock_portfolio.html',{'user':user})

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


def buy(request, pk, sn):
    if request.method=="POST":
        user = get_object_or_404(CustomUser, pk=pk)
        stock = get_object_or_404(Stock, stock_name=sn)
        stock.buy_price = stock.current_price
        quantity = int(request.POST.get("quantity-"+sn))
        stock.buy_quantity += quantity
        pdb.set_trace()
        user.total_fund -= quantity*stock.current_price
        user.save()
        stock.save()
        return render(request, '../templates/stock_portfolio.html', {'user': user})
    else:
        user = get_object_or_404(CustomUser, pk=pk)
        render(request, '../templates/stock_portfolio.html', {'user': user})

def sell(request, pk, sn):
    if request.method=="POST":
        user = get_object_or_404(CustomUser, pk=pk)
        stock = get_object_or_404(Stock, stock_name=sn)
        quantity = int(request.POST.get("quantity-"+sn))
        pdb.set_trace()
        user.total_fund += quantity*stock.current_price
        user.save()
        stock.save()
        return render(request, '../templates/stock_portfolio.html', {'user': user})
    else:
        user = get_object_or_404(CustomUser, pk=pk)
        render(request, '../templates/stock_portfolio.html', {'user': user})