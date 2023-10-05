import requests
from bs4 import BeautifulSoup
import random
import mydb
import time

cursor = mydb.conn.cursor()

now = time.ctime() #現在時間
now = time.strftime('%Y/%m/%d')
# print(now)

# url = 'https://www.soymilk.com.tw/products/all/1'
url = 'https://www.soymilk.com.tw/products/all/1?csrf_test_name=645382796de25b98753ff1083ce09d29&sorttype=&sortnum=3'

goods = requests.get(url).text
# print(goods_list)

#html解析
sp = BeautifulSoup(goods,'html.parser')
# print(sp)

#抓取圖片連結、商品連結、商品名稱、自訂價格
items = sp.find('ul',class_='products-list list-h sort-list')
# print(items)

allProduct = items.find_all('li')
# print(allProduct)

for allP in allProduct:
    photo_url = allP.find('img').get('src')
    good_url = allP.find('a').get('href')
    title = allP.find('div',class_='name').text
    # price = random.randint(30,80)   #30到80內，隨機一個整數
    price = random.randrange(30,80,5) #30到80內，以間隔5的距離隨機抽取
    pdate = now #當下寫資料的時間(僅有日期)

    sql = "insert into product(name,photo_url,goods_url,price,discount,create_date) values('{}','{}','{}','{}','{}','{}')".format(title,photo_url,good_url,price,price,pdate)

    cursor.execute(sql) #執行SQL語法
    mydb.conn.commit()  #立即提交

mydb.conn.close()       #資料抓去完畢並寫入後，才將此次資料庫連線關閉