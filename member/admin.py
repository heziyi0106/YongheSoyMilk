from django.contrib import admin

# Register your models here.

from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile') #後臺呈現姓名、email、手機號碼

admin.site.register(Member,MemberAdmin)
