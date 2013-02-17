'''
Created on Feb 10, 2013

@author: oleg
'''
from django.contrib import admin
from . import models


class TranslationInline(admin.TabularInline):
    model = models.Translation


class ImageInline(admin.TabularInline):
    model = models.InfoImage


class NewsAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('date', 'title')


class AdressInline(admin.TabularInline):
    model = models.Adress_translation


class AdressAdmin(admin.ModelAdmin):
    inlines = (
        AdressInline,
    )
    list_display = ('type',)


class TareAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class StorageConditionAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class BrandAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class ProductAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class ConsumerCategoryAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class ConsumerSubCategoryAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class ConsumerInfoAdmin(admin.ModelAdmin):
    inlines = (
        TranslationInline, ImageInline,
    )
    list_display = ('title',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class Feed_backAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Adress, AdressAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Tare, TareAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ConsumerCategory, ConsumerCategoryAdmin)
admin.site.register(models.ConsumerSubCategory, ConsumerSubCategoryAdmin)
admin.site.register(models.ConsumerInfo, ConsumerInfoAdmin)
admin.site.register(models.StorageCondition, StorageConditionAdmin)
admin.site.register(models.Feed_back, Feed_backAdmin)
