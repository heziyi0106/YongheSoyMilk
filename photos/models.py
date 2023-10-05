from django.db import models

# Create your models here.

#當django要使用上傳圖片的功能時，必須在系統上先安裝pip install pillow 套件，才可以上傳圖片

from django.utils import timezone

class Photo(models.Model):
    # upload_to 圖片上傳後，存放的路徑位置
    # blank, null 這兩個表示圖片欄位是否可以是空值，預設False
    # 若要空值，blank=True, null=True
    image = models.ImageField(upload_to='images/',blank=False,null=False)
    upload_date = models.DateField(default=timezone.now) #抓下圖片的時間