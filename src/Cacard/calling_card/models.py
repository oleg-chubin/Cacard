from django.db import models
from django.contrib import admin
from django.utils.translation import get_language
# Create your models here.


class Language(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=4)

    def __unicode__(self):
        return u'%s' % (self.name)


class Info(models.Model):
    @property
    def title(self):
        lang = get_language()
        translation = self.translation_set.filter(lang__code=lang[:2])
        if translation.count():
            return translation[0].title
        return ('No translation')

    @property
    def description(self):
        lang = get_language()
        translation = self.translation_set.filter(lang__code=lang[:2])
        if translation.count():
            return translation[0].description
        return ('No translation')


class Tare(Info):
    name = models.CharField(max_length=25)
    capacity = models.IntegerField()
    in_box = models.IntegerField('Max count in box')

    def __unicode__(self):
        return u'%s' % (self.name)


class Brand(Info):  # kama,oleyna
    image_tumboral = models.ImageField(upload_to = 'images', blank = True, null = True)
    image = models.ImageField(upload_to = 'images', blank = True, null = True)

    def __unicode__(self):
        return u'%s' % (self.title)


class ProductCategory(Info):  # oliya, maslo

    def __unicode__(self):
        return u'%s' % (self.title)


class StorageCondition(Info):

    def __unicode__(self):
        return u'%s' % (self.title)


class Product(Info):
    tare = models.ForeignKey(Tare)
    brand = models.ForeignKey(Brand)
    productcategory = models.ForeignKey(ProductCategory)
    storagecondition = models.ForeignKey(StorageCondition)


class ConsumerCategory(Info):
    image_tumboral = models.ImageField(upload_to = 'images', blank = True, null = True)
    image=models.ImageField(upload_to = 'images', blank = True, null = True)

    def __unicode__(self):
        return u'%s' % (self.title)


class ConsumerSubCategory(Info):
    image_tumboral = models.ImageField(upload_to = 'images', blank = True, null = True)
    image = models.ImageField(upload_to = 'images', blank = True, null = True)

    def __unicode__(self):
        return u'%s' % (self.title)


class ConsumerInfo(Info):
    image_tumboral = models.ImageField(upload_to = 'images', blank = True, null = True)
    image = models.ImageField(upload_to = 'images', blank = True, null = True)
    consumercategory = models.ForeignKey(ConsumerCategory)
    consumersubcategory = models.ForeignKey(ConsumerSubCategory)


class Translation(models.Model):
    info = models.ForeignKey(Info)
    title = models.CharField(max_length=250)
    description = models.TextField()
    lang = models.ForeignKey(Language)


class News(Info):
    date = models.DateField()

    class Meta:
        ordering = ('-date',)


class Adress(Info):
    type_adr = models.CharField(max_length=50)


class TranslationInline(admin.TabularInline):
    model = Translation


class NewsAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('date', 'title')


class AdressAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('type_adr', 'title')


class TareAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class StorageConditionAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class BrandAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class ProductAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class ConsumerCategoryAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class ConsumerSubCategoryAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class ConsumerInfoAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline,
    )
    list_display = ('title',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(News, NewsAdmin)
admin.site.register(Adress, AdressAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Tare, TareAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ConsumerCategory, ConsumerCategoryAdmin)
admin.site.register(ConsumerSubCategory, ConsumerSubCategoryAdmin)
admin.site.register(ConsumerInfo, ConsumerInfoAdmin)
admin.site.register(StorageCondition, StorageConditionAdmin)
