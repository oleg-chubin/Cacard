from StringIO import StringIO
from PIL import ImageFile
from django.db import models
from django.utils.translation import get_language
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.


PORTION_SIZE = 1024

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

    @property
    def info_image(self):
        if not self.infoimage_set.count():
            return
        return self.infoimage_set.order_by('-priority')[0]


class InfoImage(models.Model):
    thumbnail = models.ImageField(upload_to='images')
    image = models.ImageField(upload_to='images')
    priority = models.IntegerField()
    info = models.ForeignKey(Info)

@receiver(pre_save, sender=InfoImage)
def thumbnail_handler(sender, instance=None, **kwargs):
    if not instance.thumbnail or not isinstance(instance.thumbnail.file,
                                                InMemoryUploadedFile):
        return

    thumb_file = instance.thumbnail.file
    parser = ImageFile.Parser()
    portion = thumb_file.read(PORTION_SIZE)
    while portion:
        parser.feed(portion)
        portion = thumb_file.read(PORTION_SIZE)
    image_file = parser.close()
    size = image_file.size
    ratio = max([i / 320.0 for i in size])
    resized_image = image_file.resize([int(i / ratio) for i in size])
    thumb = StringIO()
    resized_image.save(thumb, image_file.format)
    instance.thumbnail = InMemoryUploadedFile(thumb, thumb_file.field_name,
                                              thumb_file.name,
                                              thumb_file.content_type,
                                              thumb.len, thumb_file.charset)

    return


class Feed_back(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    name = models.CharField(max_length=100)
    e_mail = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.title)


class Tare(Info):
    name = models.CharField(max_length=25)
    capacity = models.IntegerField()
    in_box = models.IntegerField('Max count in box')

    def __unicode__(self):
        return u'%s' % (self.name)


class Brand(Info):  # kama,oleyna
    def __unicode__(self):
        return u'%s' % (self.title)


class ProductCategory(Info):  # oliya, maslo

    def __unicode__(self):
        return u'%s' % (self.title)


class StorageCondition(Info):

    def __unicode__(self):
        return u'%s' % (self.title)


class Product(Info):
    tare = models.ManyToManyField(Tare)
    brand = models.ForeignKey(Brand)
    productcategory = models.ForeignKey(ProductCategory)
    storagecondition = models.ForeignKey(StorageCondition)


class ConsumerCategory(Info):
    
    def __unicode__(self):
        return u'%s' % (self.title)


class ConsumerSubCategory(Info):

    def __unicode__(self):
        return u'%s' % (self.title)


class ConsumerInfo(Info):
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


