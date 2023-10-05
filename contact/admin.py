from django.contrib import admin

# Register your models here.

from .models import Message

class MessageAdmin(admin.ModelAdmin):
    #設定後臺可見的資料欄位
    list_display = ('subject', 'email') #問題主題、信箱

admin.site.register(Message,MessageAdmin)