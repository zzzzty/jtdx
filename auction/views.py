from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Product,SellProduct
# Create your views here.


def show(request,productpk):
    content = {}
    message = ""
    product = get_object_or_404(Product,pk=productpk)
    #price = get_object_or_404(SellProduct,product_id=productpk)
    price = SellProduct.objects.filter(product_id = productpk).exists()
    if price:
        price = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')[0]
        prices = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')
    else:
        price = product.start_price
        prices = []

    content['price'] = price
    content['prices'] = prices
    content['product'] = product
    #
    
    if request.method == "POST":
        belong_ = request.POST.get('belong_','请输入姓名')
        request.session['belong_'] = belong_
        if belong_ == "请输入姓名":
            message="输入姓名"
        else:
            price_ = request.POST.get('price_')
            try:
                if len(prices)>0:
                    maxprice = prices[0].price
                else:
                    maxprice = price
                if int(price_) > maxprice:
                    newsell = SellProduct()
                    newsell.product = product
                    newsell.belong = belong_
                    newsell.price = price_
                    newsell.save()
                    print("sssssssssssss")
                else:
                    message="有人出高价格了"
            except:
                message="价格底了"
        
    if request.method == 'GET':
        belong_="请输入姓名"
        belong_=request.session.get('belong_','请输入姓名')
    content['belong_'] = belong_
    content['message'] = message
    prices = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')
    content['prices'] = prices
    return render(request,"auction/product.html",content) 


def bigshow(request,productpk):
    content = {}
    message = ""
    product = get_object_or_404(Product,pk=productpk)
    #price = get_object_or_404(SellProduct,product_id=productpk)
    price = SellProduct.objects.filter(product_id = productpk).exists()
    if price:
        price = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')[0]
        prices = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')
    else:
        price = product.start_price
        prices = []

    content['price'] = price
    content['prices'] = prices
    content['product'] = product
    prices = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')
    content['prices'] = prices
    return render(request,"auction/bigproduct.html",content) 
