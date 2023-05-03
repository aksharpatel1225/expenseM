# Register your models here.
from django.contrib import admin
from .models import Category
from.models import Subcategory
from.models import Label
from.models import Payee
from.models import Accounttype
from.models import Currencytype
from.models import Account
from.models import  Expense 

# Register your models here.


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Label)
admin.site.register(Payee)
admin.site.register(Accounttype)
admin.site.register(Currencytype)
admin.site.register(Account)
admin.site.register(Expense)