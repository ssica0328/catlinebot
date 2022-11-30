from django.db import models

# Create your models here.

class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    ansdt = models.DateTimeField(auto_now=True)                         #User回答每日一問的時間
    points = models.IntegerField(null=False,default=0)                  #分數

    def __str__(self):
        return self.uid

class random_exam(models.Model):
    num = models.IntegerField(null=False,default=0)
    question = models.CharField(max_length=255,blank=True,null=False,default='')
    op1 = models.CharField(max_length=255,blank=True,null=False,default='')
    op2 = models.CharField(max_length=255,blank=True,null=False,default='')
    op3 = models.CharField(max_length=255,blank=True,null=False,default='')
    ans = models.IntegerField(null=False,default=0)

    def __int__(self):
        return self.num

class 乖乖吃飯(models.Model):
    num = models.IntegerField(null=False,default=0)
    name = models.CharField(max_length=255,blank=True,null=False,default='')
    price = models.CharField(max_length=255,blank=True,null=False,default='')
    grams = models.CharField(max_length=255,blank=True,null=False,default='')
    protein = models.CharField(max_length=255,blank=True,null=False,default='')
    fat = models.CharField(max_length=255,blank=True,null=False,default='')
    carbo = models.CharField(max_length=255,blank=True,null=False,default='')
    phos = models.CharField(max_length=255,blank=True,null=False,default='')
    kcal = models.CharField(max_length=255,blank=True,null=False,default='')
    score = models.IntegerField(null=False,default=0)

    def __int__(self):
        return self.num

class 心靈雞湯(models.Model):
    num = models.IntegerField(null=False,default=0)
    name = models.CharField(max_length=255,blank=True,null=False,default='')
    price = models.CharField(max_length=255,blank=True,null=False,default='')
    grams = models.CharField(max_length=255,blank=True,null=False,default='')
    protein = models.CharField(max_length=255,blank=True,null=False,default='')
    fat = models.CharField(max_length=255,blank=True,null=False,default='')
    carbo = models.CharField(max_length=255,blank=True,null=False,default='')
    phos = models.CharField(max_length=255,blank=True,null=False,default='')
    score = models.IntegerField(null=False,default=0)

    def __int__(self):
        return self.num


class pidan(models.Model):
    num = models.IntegerField(null=False,default=0)
    name = models.CharField(max_length=255,blank=True,null=False,default='')
    price = models.CharField(max_length=255,blank=True,null=False,default='')
    grams = models.CharField(max_length=255,blank=True,null=False,default='')
    material = models.CharField(max_length=255,blank=True,null=False,default='')
    ratio = models.CharField(max_length=255,blank=True,null=False,default='')
    score = models.IntegerField(null=False,default=0)

    def __int__(self):
        return self.num

class toy(models.Model):
    num = models.IntegerField(null=False,default=0)
    name = models.CharField(max_length=255,blank=True,null=False,default='')
    price = models.CharField(max_length=255,blank=True,null=False,default='')
    score = models.IntegerField(null=False,default=0)

    def __int__(self):
        return self.num



