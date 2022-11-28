from django.contrib import admin

# Register your models here.
from cat_linebot.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'pic_url', 'mtext', 'mdt', 'points')
admin.site.register(User_Info,User_Info_Admin)

class random_exam_Admin(admin.ModelAdmin):
    list_display = ['num', 'question', 'op1', 'op2', 'op3', 'ans']
admin.site.register(random_exam,random_exam_Admin)

class 乖乖吃飯_Admin(admin.ModelAdmin):
    list_display = ['num', 'price', 'grans', 'protein', 'fat', 'carbo', 'phos', 'kcal', 'score']
admin.site.register(乖乖吃飯,乖乖吃飯_Admin)