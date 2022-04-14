from django import forms
from .models import diary_table,Account
from django.contrib.auth.models import User

class DiaryForm(forms.ModelForm):
    class Meta:
        model = diary_table
        fields = ('date','title','text','image')
        
        #excludeに設定したフィールドは、userがformに入力しない
        
    
class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")
    class Meta:
        model=User
        fields=('username','email','password',)
        labels={'username':'ユーザーID','email':"メール"}
        
class AccountForm_image(forms.ModelForm):
    class Meta:
        model=Account
        fields=('profile_image',)
        labels={'profile_image':"プロフィールイメージ"}