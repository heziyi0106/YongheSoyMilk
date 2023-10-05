from django.db import models

# Create your models here.

#訂單是配別人的資料表(要記錄資料表來源、名字是什麼)；一個訂單幾個產品(一對多)==>兩個資料表(1.訂單、2.訂單的細節)

class OrderModel(models.Model): #訂單資料表
    subtotal = models.IntegerField(default=0) #商品金額
    shipping = models.IntegerField(default=0) #運費
    grandtotal = models.IntegerField(default=0) #總計
    customname = models.CharField(max_length=100)
    customemail = models.CharField(max_length=100)
    customphone = models.CharField(max_length=50)
    paytype = models.CharField(max_length=20) #付款方式(可以轉到其他頁面)
    create_date = models.DateTimeField(auto_now_add=True) #訂單建立時間
    customaddress = models.CharField(max_length=200) #地址
    bankaccount = models.CharField(max_length=10,null=True) #銀行匯款帳號後五碼(允許空值)

    def __str__(self): #改寫
        return self.customname
    
class DetailModel(models.Model): #訂單明細
    #[重要]外來鍵，有指定那一個資料表為我的外來鍵。
    #每個資料表DB都有一個主鍵 primary key
    #在另一個資料表中有包含 A 資料表中的主鍵時，稱為外來鍵(此處為 OrderModel 的主鍵)
    dorder = models.ForeignKey('OrderModel',on_delete=models.CASCADE)
    pname = models.CharField(max_length=100) #產品名稱
    unitprice = models.IntegerField(default=0) #單位價格
    quantity = models.IntegerField(default=0) #訂單數量
    dtotal = models.IntegerField(default=0) #總計

    def __str__(self):
        return self.pname

