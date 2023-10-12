from django.shortcuts import render,redirect

from django.http import HttpResponseRedirect

# 也可寫from cart.models import OrderModel,DetailModel
from cart import models

from product.models import Goods #崁入產品的Goods資料表
from django.utils.html import format_html

#崁入綠界 ECPay SDK
#第二步
import os
basedir = os.path.dirname(__file__) #抓取目前預設目錄的位置
file = os.path.join(basedir,'ecpay_payment_sdk.py')

#第一步
import importlib.util
spec = importlib.util.spec_from_file_location('ecpay_payment_sdk',file) #第三步--改成自己的路徑
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

# Create your views here.
cartlist = list()   #購物車列表
customname = ''     #客戶姓名
customphone = ''    #客戶電話
customaddress = ''
customemail = ''    #客戶email

orderTotal = 0      #訂單總額
goodsTitle = list() #放入至購物車的商品名稱

#購物車的功能
def cart(request):  #顯示購物車內容
    global cartlist #宣告拿外面的變數來用

    #抓進產品列表頁面(使用goodlist變數，就不會修改到全域變數)==>貨品/購物車列表
    goodslist = cartlist 

    total = 0 #總價為0
    for unit in cartlist:
        total += int(unit[3])   #產品中每一筆的總額

    #購物滿300元，免運費
    if total >= 300:
        grandtotal = total
    else:
        grandtotal = total + 100

    # 購物車如果為空
    if len(goodslist) == 0:
        empty = 1
    else:
        empty = 0
    
    return render(request,'cart.html',locals())


#將商品加入購物車，並沒有將資料寫入資料表中(此有用到判斷購物車內的動作是哪種:ctype)
# 傳送的動作預設None，代表有值沒值都可以通過，故可供兩個路徑(url)使用
def addtocart(request,ctype=None,productid=None):
    global cartlist #宣告拿外部的變數來修改

    #新增 動作
    if ctype == 'add':
        product = Goods.objects.filter(id=productid).count()
        #因不確定使用者有無資料或是使用者亂操作，導致code壞掉，所以此處先用filter先過濾一遍產品

        if product > 0: #有找到產品
            product = Goods.objects.get(id=productid) #確定找到產品後用get(雙重確認)
            #預設購物車中都沒有相同的物品：表示此購物車內沒有這個商品，用flag = True表示
            flag = True

            #用程式檢查購物車中是否有重複的值
            for unit in cartlist: #將產品列表一個個抓取出來
                if product.name == unit[0]: #抓出的產品項目是否等於資料庫中的商品名稱
                    unit[2] = str(int(unit[2]) + 1) #數量+1
                    unit[3] = str(int(unit[3]) + product.price) #價格加上去
                    flag = False #表示有相同商品，已修改數量
                    break #只修改數量，就不再往下進行新增資料
            
            if flag: #購物車沒有此商品，就將商品加入至購物車中
                templist = list()
                templist.append(product.name)
                templist.append(str(product.price)) #產品的價格
                templist.append('1') #產品的數量
                templist.append(str(product.price)) #產品的總額
                cartlist.append(templist)

            #unit[0] 商品名稱
            #unit[1] 商品價格
            #unit[2] 商品數量
            #unit[3] 商品總價
            request.session['cartlist'] = cartlist
            #把購物車寫回session
            return redirect('/cart/') #加入商品後就跳轉回購物車頁
        
        else: #product<=0 的狀況(沒有商品)
            #表示沒有這個商品id，直接導回產品頁面，讓使用者去做動作
            return redirect('/product/')
    
    #修改購物車數量 的動作
    elif ctype == 'update':
        n = 0
        for unit in cartlist: #無法知道哪一個被修改，故一個個將項目抓出來(cart.html搭配模板語言)
            amount = request.POST.get('qty'+str(n),'1') #抓不到東西時，預設數量為1
            if len(amount) == 0: #雙重確認
                amount = '1'
            if int(amount) <= 0: #避免被惡搞
                amount = '1'

            unit[2] = amount #數量
            unit[3] = str( int(unit[1]) * int(unit[2]) ) #總價
            n += 1
        request.session['cartlist'] = cartlist
        return redirect('/cart/') #跳轉回購物車
    
    #刪除購物車項目 動作
    elif ctype == 'delete':
        del cartlist[int(productid)] #刪除其索引值位置
        request.session['cartlist'] = cartlist #更新session
        return redirect('/cart/')
    
    #清空購物車所有項目 動作
    elif ctype == 'empty':
        cartlist = list() #清空購物車串列
        request.session['cartlist'] = cartlist
        return redirect('/cart/') #redirect是不帶任何參數過去的導轉
    

#結帳
def cartorder(request):
    #要登入，才能結帳
    if 'memMail' in request.session and 'yhm' in request.session:
        global cartlist,customname,customphone,customemail,customaddress

        total = 0 #總價為0
        goodslist = cartlist

        for unit in cartlist:
            total += int(unit[3])
        
        if (total >= 300) or (total == 0): #假設滿300元免運費
            extra = 0
        else:
            extra = 100
        grandtotal = total + extra

        name = customname
        phone = customphone
        address = customaddress
        email = request.session['memMail']

        return render(request,'cartorder.html',locals())
    
    else:
        return redirect('/login/')
    
#確認購物車寫進資料庫，並清空購物車
def cartok(request):

    #要做防範(避免有人亂搞)==>是否登入了? POST是否在這裡面? 判斷有無從該網頁送出? 不是隨便丟資料過來?
    if 'memMail' in request.session and 'yhm' in request.session:
        #二次確認
        if 'cuName' in request.POST: #該name有在這個網頁裡面，就可以抓
            global cartlist,customname,customphone,customemail,customaddress,orderTotal,goodsTitle

            total = 0
            for unit in cartlist:
                total += int(unit[3])

            if total < 300: #小於300會有運費
                shipping = 100
            else:
                shipping = 0
            grandtotal = total + shipping
            orderTotal = grandtotal #訂單總額(將值傳給全域變數)

            #將新資料蓋回去
            customname = request.POST.get('cuName','')
            customphone = request.POST.get('cuPhone')
            customaddress = request.POST.get('cuAddr')
            customemail = request.POST.get('cuEmail')
            payType = request.POST.get('payType')

            #訂單分別要寫入 訂單、訂單明細資料表中
            unitorder = models.OrderModel.objects.create(subtotal=total,shipping=shipping,grandtotal=grandtotal,customname=customname,customphone=customphone,customemail=customemail,customaddress=customaddress,paytype=payType)

            #新增明細
            for unit in cartlist:
                goodsTitle.append(unit[0]) #將商品名稱新增到串列中
                total = int(unit[1]) * int(unit[2]) #價格*數量
                #外來鍵要放入。新增訂單後，會回傳該筆的訂單資料(用外來鍵將明細跟訂單資料串在一起)
                unitdetail = models.DetailModel.objects.create(dorder=unitorder,pname=unit[0],unitprice=unit[1],quantity=unit[2],dtotal=total)

            #訂單明細新增完後，再取得以下資料和資料清除
            orderid = unitorder.id #取得訂單編號
            name = unitorder.customname
            email = unitorder.customemail
            cartlist = list()
            request.session['cartlist'] = cartlist

            #根據付款方式不同，跳轉不同頁面
            if payType == '信用卡':
                return HttpResponseRedirect('/creditcard', locals())
            else: #現金付款、轉帳
                return render(request,'cartok.html',locals())
            
    else:
        return redirect('/login/')
    
#查看單筆訂單資料
def cartordercheck(request):

    if 'orderid' in request.GET and 'customemail' in request.GET:
        orderid = request.GET.get('orderid','')
        customemail = request.GET.get('customemail','')

        if orderid == '' or customemail == '':
            nosearch = 1 #沒找到使用者
        else:
            order = models.OrderModel.objects.filter(id=orderid,customemail=customemail).first() #用first() 表示只抓取第一筆資料

            if order == None:
                notfound = 1 #沒找到訂單
            else:
                details = models.DetailModel.objects.filter(dorder=order)
            
    return render(request,'cartordercheck.html',locals())

#查看我的訂單列表
def myorder(request):

    if 'memMail' in request.session and 'yhm' in request.session:

        email = request.session['memMail']
        
        order = models.OrderModel.objects.filter(customemail=email)
        
        return render(request,"myorder.html",locals())
    else:
        return HttpResponseRedirect('/login')

#刷卡函式--串接綠界刷卡
def ECPayCredit(request):
    
    global goodsTitle
    
    title = ''
    for unit in goodsTitle:
        title += unit + "#" #因為多個商品時，需要用到 # 來隔開
    
    
    # 訂單資訊
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',  #訂單ID
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal, #總額
        'TradeDesc': 'Wendy的測試刷卡單', #詳細
        'ItemName': title, #商品名稱
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet', #回傳後，跳到聯成首頁
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet', #修改跳到聯成首頁
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet', #修改跳到聯成首頁
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html) #格式化html，將文字的html 轉換為網頁的html
        
        # print(html) #不能印，而是傳資料回前台
        return render(request,'paycredit.html',locals())   
    
    except Exception as error:
        print('An exception happened: ' + str(error))

#回報匯款後5碼
def reportBank(request):
    if 'orderid' in request.GET and 'customemail' in request.GET:
        orderid = request.GET.get('orderid','')
        customemail = request.GET.get('customemail','')

        if orderid != '' and customemail != '':
            #開始查詢，先filter，確認有了以後才用get
            bank = models.OrderModel.objects.filter(id=orderid,customemail=customemail,paytype='ATM轉帳')

            if bank == None: #找不到此訂單
                return render(request,'product.html')
            else:
                return render(request,'bankfive.html',locals())
            
        else:
            return render(request,'index.html')
    else:
        return render(request,'index.html')
    
#後五碼回報成功
def bankfiveok(request):
    if 'orderid' in request.POST:
        orderid = request.POST['orderid'] #抓到網頁表格內的值
        bankfive = request.POST['bankfive']
        email = request.session['memMail']

        obj = models.OrderModel.objects.filter(id=orderid,customemail=email).count()

        if obj > 0:
            bank = models.OrderModel.objects.get(id=orderid)
            bank.bankaccount = bankfive #修改值
            bank.save()

            order = models.OrderModel.objects.filter(customemail=email) #get只能抓一個，filter則抓多個

            return render(request,'myorder.html',locals())

    else:
        return render(request,'index.html')       