from django.db import models
from django.contrib import admin
# Create your models here.


class Info(models.Model):
    pass

class Translation(Info):
    date=models.DateField(default='01.01.2013')
    title=models.CharField(max_length=250)
    description=models.TextField()
    title_ua=models.CharField(max_length=250)
    description_ua=models.TextField()
    title_en=models.CharField(max_length=250)
    description_en=models.TextField()
    

class News(Translation):
    class Meta:
        ordering = ('date',)

class Adress(Translation):
    type_adr=models.CharField(max_length=50)



class NewsAdmin(admin.ModelAdmin):
    list_display = ('date','title')
    
class AdressAdmin(admin.ModelAdmin):
    list_display = ('type_adr','title')


admin.site.register(News,NewsAdmin)
admin.site.register(Adress,AdressAdmin)
