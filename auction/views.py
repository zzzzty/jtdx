from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Product,SellProduct
# Create your views here.


def show(request,productpk):
    content = {}
    product = get_object_or_404(Product,pk=productpk)
    #price = get_object_or_404(SellProduct,product_id=productpk)
    price = 0
    price = SellProduct.objects.filter(product_id = productpk).count()
    if price > 0:
        prices = SellProduct.objects.filter(product_id = productpk).order_by('-create_time')
    else:
        prices = 50
    content['price'] = price
    content['prices'] = prices
    content['product'] = product

    if request.method == "POST":
        price_ = request.POST.get('price_')
        belong_ = request.POST.get('belong_')
        newsell = SellProduct()
        newsell.product=product
        newsell.belong = belong_
        newsell.price = price_
        newsell.save()
    
    return render(request,"auction/product.html",content) 