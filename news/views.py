from django.shortcuts import render

from django.http import HttpResponse

from .models import myNews
# Create your views here.

from product.models import Goods #要使用產品資料庫的內容

def news(request):
    data = myNews.objects.all().order_by('-id')
    # myNews.objects是物件(admin後臺顯示的)；all()全部；order_by排序；-id表示依據id的欄位做遞減排序，沒-表示遞增排序
    content = {'news_list':data}
    #可以把(資料庫中)該傳的東西丟回給網頁顯示==>1.字典方式 2.locals()

    return render(request,'news.html',content)

def index(request):
    product = Goods.objects.all().order_by('-id')[:4] #產品列表1-4
    data = myNews.objects.all().order_by('-id')[:4] #新聞列表1-4
    return render(request,'index.html',locals())