from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
 
 
class diary_table(models.Model):
    #on_delete=models.PROTECTは関連するオブジェクトがあると削除できない。
    #ForeignKey    多対一
    #OneToOneField    一対一
    #ManyToManyField    多対多

    user = models.ForeignKey(User,verbose_name='ユーザー',on_delete=models.PROTECT,blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name='日付', default=timezone.now)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    text = models.CharField(verbose_name='本文', max_length=200)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='編集日時', blank=True, null=True)
    
class Account(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class ProductA(models.Model):
    #Datetime.dateを保存するフィールド
    Date = models.DateField()
    
    #IntegerField    -2147483648 to 2147483647の値の整数のフィールド。
    Revenue = models.IntegerField()
    
    