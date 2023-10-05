from django.contrib import admin

# Register your models here.

from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    #自訂顯示圖片
    list_display = ('image','upload_date') #顯示這兩個欄位

admin.site.register(Photo,PhotoAdmin)
