from django.contrib import admin

# Register your models here.

from .models import Goods

#自訂後臺顯示格式
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'create_date')
    #自訂顯示的欄位

#註冊
admin.site.register(Goods,GoodsAdmin)