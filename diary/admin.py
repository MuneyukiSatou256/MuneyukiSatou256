from django.contrib import admin

# Register your models here.

from .models import Account,diary_table,ProductA

admin.site.register(Account)
admin.site.register(diary_table)
admin.site.register(ProductA)