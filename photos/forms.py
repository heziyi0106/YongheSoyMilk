# 上傳圖片時必須使用這個檔案

from django import forms
from .models import Photo

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)
        widgets = {
            'images':forms.FileInput(attrs=
            {'class':'form-control-file'})
        }