from django.db import models

# Create your models here.

#會員資料
class Member(models.Model):
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
    birthday = models.DateField()
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    c_date = models.DateField(auto_now_add=True) #建立會員資料的時間

    class Meta:
        db_table = 'associator'  #django不給建立名為member的資料表==>命名為associator會員