from django.db import models
from django.contrib import admin
import datetime
# Create your models here.


class Translation(models.Model):
    date=models.DateField(default=datetime.date(2001,01,01))
    title=models.CharField(max_length=250)
    description=models.TextField()
    title_ua=models.CharField(max_length=250)
    description_ua=models.TextField()
    title_en=models.CharField(max_length=250)
    description_en=models.TextField()
    
class Info(models.Model):
    translate=models.ForeignKey(Translation)


class News(Info):
    pass

class Adress(Info):
    type_adr=models.CharField(max_length=50)


class NewsAdmin(admin.ModelAdmin):
    pass
    
class AdressAdmin(admin.ModelAdmin):
    list_display = ('type_adr',)




admin.site.register(News,NewsAdmin)
admin.site.register(Adress,AdressAdmin)
