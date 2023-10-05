from django.db import models

# Create your models here.
class myNews(models.Model): #繼承自models.Model
    title = models.CharField(max_length=100) #新聞標題
    content = models.TextField()  #新聞內容
    photo_url = models.CharField(max_length=200) #新聞網址
    create_date = models.DateTimeField(auto_now_add=True) #新聞建立/發布後的當下時間，系統自行建立

    class Meta: #class內部的class
        db_table = 'news'
        #必寫，系統才會正確建立該字串內名稱的資料表
