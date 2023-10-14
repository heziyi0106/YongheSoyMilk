from django.shortcuts import render,redirect

# Create your views here.

from .forms import UploadModelForm
from .models import Photo

def uploadFile(request):
    photos = Photo.objects.all().order_by('-id')    #抓取全部的資料
    form = UploadModelForm()        #建立上傳圖片表單物件
    
    if request.method == 'POST':    #確定上傳是否為POST
        #從網頁中，將檔案直接上傳至網站伺服器中
        form = UploadModelForm(request.POST,request.FILES)
        
        if form.is_valid(): #表單是否有效/上傳(使用者輸入的訊息是否正確)
            form.save()     #儲存表單到forms.py
            return redirect('/photos')
    
    context = {
        'photos' : photos,
        'form' : form
        }
    return render(request,'photos.html',locals())            
        