"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from news.views import news,index
from product.views import product
from contact.views import contact
from member.views import register,login,logout,changepassword
from cart.views import cart,addtocart,cartorder,cartok,cartordercheck,myorder,ECPayCredit,reportBank,bankfiveok

#抓媒體檔案需要下面兩行(檔案的上傳，必須將settings裡面的資料抓到urls裡面的網址去，才可以往上丟。)
from django.conf import settings
from django.conf.urls.static import static #將設定檔的內容抓進來
from photos.views import uploadFile

urlpatterns = [
    path("admin/", admin.site.urls),
    path('news/',news), #網址,函式
    path('',index),
    path('product/',product),
    path('contact/',contact),
    path('register/',register),
    path('login/',login),
    path('logout/',logout),
    path('changepassword/',changepassword),
    path('cart/',cart),
    path('addtocart/<str:ctype>/<int:productid>/',addtocart), #帶入文字str/數字int:參數的名稱(自訂)
    path('addtocart/<str:ctype>/',addtocart),
    path('cartorder/',cartorder),
    path('cartok/',cartok),
    path('cartordercheck/',cartordercheck),
    path('myorder/',myorder),
    path('creditcard/',ECPayCredit),
    path('reportBank/',reportBank),
    path('bankfiveok/',bankfiveok),
    path('photos/',uploadFile),
]

#新增判斷式(是否有DEBUG)來導入設定檔的網址。
if settings.DEBUG: 
     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
