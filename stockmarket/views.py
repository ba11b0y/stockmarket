from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
# from stockmarket.forms import LoginForm
from .models import CustomUser, Stock, Buy_Data
import requests
import json
import pdb
# Create your views here.
def get_stock_price(stock_name):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stock_name+"&interval=5min&apikey=ZJL36WNK4F9QOJNF"
    stock_data = requests.get(url)
    stock_json = json.loads(stock_data.content)
    last_refresh = stock_json["Meta Data"]["3. Last Refreshed"]
    price = float(stock_json["Time Series (5min)"][last_refresh]["4. close"])
    return price


def successful_login(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    allstocks = user.stocks.all()
    #pdb.set_trace()
    for stock in allstocks:
        stock.current_price = get_stock_price(str(stock.name))
        buy_data = stock.buy_data_set.all().filter(user=user)
        if len(buy_data)==0:
            buy_data_new = Buy_Data(user=user, stock=stock,price=[0.0],quantity=[0])
            buy_data_new.average_price = buy_data_new.get_average_price()
            buy_data_new.save()
            stock.save()
            user.save()
        else:
            buy_data = buy_data[0]
            buy_data.average_price = buy_data.get_average_price()
            buy_data.save()
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

@login_required(login_url='login')
def buy(request, pk, sn):
    err=""
    if request.method=="POST":
        user = get_object_or_404(CustomUser, pk=pk)
        stock = get_object_or_404(Stock, name=sn)
        buy_data = stock.buy_data_set.all()[0]
        quantity = float(request.POST.get("quantity-"+sn))
        if quantity<0:
            err="Quantity can't be negative!"
            return render(request,'../templates/stock_portfolio.html',{'user':user,'err':err})
        else:
            if stock.current_price*quantity>user.total_fund:
                err="You don't have this much fund!"
                return render(request, '../templates/stock_portfolio.html', {'user': user,'err':err})
            buy_data.price.append(stock.current_price)
            buy_data.quantity.append(quantity)
            buy_data.average_price = buy_data.get_average_price()
            user.total_fund-=quantity*stock.current_price
            #pdb.set_trace()
            buy_data.save()
            user.save()
            stock.save()
            return render(request, '../templates/stock_portfolio.html', {'user': user})

    else:
        user = get_object_or_404(CustomUser, pk=pk)
        render(request, '../templates/stock_portfolio.html', {'user': user})
@login_required
def sell(request, pk, sn):
    err=""
    if request.method=="POST":
        user = get_object_or_404(CustomUser, pk=pk)
        stock = get_object_or_404(Stock, name=sn)
        buy_data = stock.buy_data_set.all()[0]
        quantity = float(request.POST.get("quantity-"+sn))
        qcopy = quantity
        l=len(buy_data.quantity)
        pdb.set_trace()
        for i in range(l-1,0,-1):
            if qcopy>0:
                if quantity>sum(buy_data.quantity):
                    err="The entered quantity of the stock is greater than you own!"
                    return render(request, '../templates/stock_portfolio.html', {'user': user,'err':err})
                else:
                    if quantity<=buy_data.quantity[i]:
                        buy_data.quantity[i]-=quantity
                        user.total_fund += quantity*stock.current_price
                        qcopy=0
                        #pdb.set_trace()
                        user.save()
                        buy_data.save()
                        stock.save()
                        return render(request, '../templates/stock_portfolio.html', {'user': user})
                    else:
                        del buy_data.quantity[i]
                        del buy_data.price[i]
                        user.total_fund += quantity*stock.current_price
                        qcopy-=quantity
            else:
                err=" Quantity can't be negative!"
                return render(request, '../templates/stock_portfolio.html', {'user': user,'err':err})
        #pdb.set_trace()
    else:
        user = get_object_or_404(CustomUser, pk=pk)
        return render(request, '../templates/stock_portfolio.html', {'user': user})