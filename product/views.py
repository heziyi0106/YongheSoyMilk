from django.shortcuts import render

from .models import Goods

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

def product(request):

    #價格篩選器
    goods = '' #商品一開始為空
    startprice = ''
    endprice = ''

    #從html上找到產品的資料後
    if 'qgoods' in request.GET:
        goods = request.GET['qgoods']
        startprice = request.GET['startp'] #GET的參數要跟html中的name一樣
        endprice = request.GET['endp']

        #有商品、但沒有設定價格範圍的區間
        if ( len(goods) > 0 and len(startprice) == 0 and len(endprice) == 0):

            #從資料庫中先篩選出所有商品再以降序的方式顯示
            data = Goods.objects.filter(name__contains=goods).order_by('-id')

        #沒商品、最低價格有數字、最高價格有數字
        elif ( len(goods) == 0 and len(startprice) > 0 and len(endprice) > 0 ):

            #從資料庫中先用價格篩選出商品再以降序的方式顯示
            data = Goods.objects.filter(price__gte=startprice,price__lte=endprice).order_by('-id')

        #有商品、有最低價、有最高價
        elif ( len(goods) > 0 and len(startprice) > 0 and len(endprice) > 0 ):

            data = Goods.objects.filter(name__contains=goods,price__gte=startprice,price__lte=endprice).order_by('-id')

        else:
            #顯示全部的商品資料
            data = Goods.objects.all().order_by('-id')

    else:
        #顯示全部的商品資料
        data = Goods.objects.all().order_by('-id')

    #分頁
    paginater = Paginator(data,8) #12個商品為一頁
    page = request.GET.get('page') #用明碼抓取網頁內容

    #例外
    try:
        data = paginater.page(page)
    except PageNotAnInteger: #當page不是整數時
        data = paginater.page(1) #控制頁數，回到第一頁
    except EmptyPage:
        data = paginater.page(paginater.num_pages)
        #跳到最後一頁(自動計算)



    
    return render(request,'product.html',locals())