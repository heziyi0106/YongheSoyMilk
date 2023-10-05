from django.contrib import admin

# Register your models here.
from .models import myNews

#自訂後來顯示格式
class myNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date')

admin.site.register(myNews,myNewsAdmin)

