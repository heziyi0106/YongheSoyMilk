from django.shortcuts import render

# Create your views here.

from .models import Message

def contact(request):
    
    #檢查使用者是否有點擊表單送出，檢查其中一個輸入值的name
    if 'userName' in request.POST:
        name = request.POST['userName'] #post的資料要從網頁取得
        email = request.POST['uemail']
        subject = request.POST['usubject']
        content = request.POST['ucontent']

        #新增資料到資料表中(參數=外部傳來的變數名稱)
        obj = Message.objects.create(name=name, email=email, subject=subject, content=content)

        obj.save() #存檔

    return render(request,'contact.html')