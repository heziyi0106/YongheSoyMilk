from django.shortcuts import render
import hashlib
from .models import Member
from django.http import HttpResponseRedirect,HttpResponse #做會員登入後導轉頁面使用

# Create your views here.

def login(request): #登入
    msg = ''
    
    if 'email' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        # 將密碼加密
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()

        #過濾輸入的資料有無在資料庫內
        obj = Member.objects.filter(email=email,password=password).count()

        if obj > 0: #有會員，要導轉至某頁面
            #儲存資料有兩種：　session 和 cookie
            #1.建立 session 物件
            # 可以將值 暫時儲存在 伺服器端，當瀏覽器關閉時，session內的值就會不見；當使用者在重新開啟瀏覽器時，就會抓不到值(限定當下的瀏覽器)
            # 當使用者打開瀏覽器時，它會主動跟伺服器端抓取一個id，id每次都不同

            #2.Cookie 將資料儲存在使用者的電腦中一個小檔案

            #建立session(自訂key名稱)
            request.session['memMail'] = email #將email值存入session中
            request.session['isAlive'] = True #確定網頁有存著資料(登入狀態)(無論有無關閉網頁都存在)
            request.session['yhm'] = 'good' #此資料可自己決定

            #加入Cookie 功能，但須注意的是：若使用著禁用Cookie時，就會失效。
            response = HttpResponseRedirect('/') #登入後儲存cookie前，要先轉向某路徑(網站的根目錄=首頁)，cookie才可以利用此物件來記錄==>成功登入的話才轉向

            # max_age=秒，表示在這個網站中，Cookie的這個變數UMail只能存活1200秒
            response.set_cookie('UMail',email,max_age=1200)

            return response
        
        else:
            msg = '帳密錯誤，請重新輸入！'
            return render(request,'login.html',locals())

    else: #沒有登入時，網頁會跳回login.html
            return render(request,'login.html',locals())
        
def logout(request): #登出
    #登出後要清掉資料，網頁可以跳至任何一個頁面

    #有兩種刪除的方法
    #1.刪除指定的 session 變數，及其內容
    del request.session['memMail']
    del request.session['isAlive']
    del request.session['yhm']

    #2.刪除目前所有的session值
    request.session.clear()

    #刪除 cookie 的值
    response = HttpResponseRedirect('/') #頁面導轉到首頁
    response.delete_cookie('UMail')

    return response

def register(request): #註冊
    msg = ''

    if 'uName' in request.POST:
        uname = request.POST['uName']
        uemail = request.POST['uEmail']
        password = request.POST['uPassword']
        sex = request.POST['uSex']
        birthday = request.POST['uBir']
        address = request.POST['uAddr']
        mobile = request.POST['uTel']

        #加密
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest() #django要選擇sha_256的加密方式，才會正常

        #抓email有無在資料庫內，語法要用"過濾"的。若資料庫內必有資料，則用objects.get(id=?)，否則用objects.filter。
        obj = Member.objects.filter(email=uemail).count() #傳回查詢筆數

        if obj == 0: #筆數0，表示沒有這個會員
            #建立使用者
            Member.objects.create(name=uname,email=uemail,password=password,sex=sex,birthday=birthday,address=address,mobile=mobile)

            msg = '已完成註冊，請登入'
        else:
            msg = '此 email 已註冊過，請換一個email 註冊'

    return render(request,'register.html',locals())

def changepassword(request):
    #判斷使用者是否已經登入了。若沒有登入，直接使用該頁面時，就會先導回登入頁面。

    if 'memMail' in request.session and 'yhm' in request.session:
        #先檢查舊密碼是不是符合資料庫內的資料(將輸入的密碼加密後去問資料表)，符合=可更改；不符合=不給更改

        msg = '' #提示用

        if 'oldpwd' in request.POST:
            #原碼
            oldpwd = request.POST['oldpwd']
            newpwd = request.POST['newpwd']

            #原碼加密
            oldpwd = hashlib.sha3_256(oldpwd.encode('utf-8')).hexdigest()
            newpwd = hashlib.sha3_256(newpwd.encode('utf-8')).hexdigest()

            #從session 抓取使用者登入時的email
            email = request.session['memMail'] #session的變數若有需要，再另外建立就好

            #查詢(過濾)資料表中是否有該使用者的email和oldpwd
            obj = Member.objects.filter(email=email,password=oldpwd).count()

            if obj > 0: #有該使用者
                #使用 get 抓出，表示這個資料表中一定有此 email，然後修改再儲存
                user = Member.objects.get(email=email)
                user.password = newpwd
                user.save()
                msg = '密碼變更成功！！'

            else:
                msg = '舊密碼錯誤，請重新輸入再變更！！'

        return render(request,'changepassword.html',locals())
    
    else:
        return HttpResponseRedirect('/login')