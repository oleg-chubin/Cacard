from django.db import models
from django.contrib import admin
import datetime

from django.utils.translation import get_language
# Create your models here.


class Language(models.Model):
    name=models.CharField(max_length=25)
    code=models.CharField(max_length=4)


class Info(models.Model):
    @property
    def title(self):
        lang = get_language()
        translation = self.translation_set.filter(lang__code=lang[:2])
        if translation.count():
            return translation[0].title
        return _('No translation')


class Translation(models.Model):
    info=models.ForeignKey(Info)
    title=models.CharField(max_length=250)
    description=models.TextField()
    lang=models.ForeignKey(Language)
    
class News(Info):
    date=models.DateField()
    pass

class Adress(Info):
    type_adr=models.CharField(max_length=50)


class NewsAdmin(admin.ModelAdmin):
    pass
    
class AdressAdmin(admin.ModelAdmin):
    list_display = ('type_adr',)




admin.site.register(News,NewsAdmin)
admin.site.register(Adress,AdressAdmin)
