from StringIO import StringIO
from PIL import ImageFile
from django.db import models
from django.forms import ModelForm
from django.utils.translation import get_language
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile

from Cacard.client_management.models import Client
# Create your models here.


PORTION_SIZE = 1024


#class ClientAwareModel(models.Model):
#    client = models.ForeignKey(Client,
#                               related_name="%(app_label)s_%(class)s_related")
#
#    class Meta:
#        abstract = True

class CommonDate(models.Model):
    pass


class DateRule(models.Model):
    DURATION = ((1, "Day"), (2, "Hour"), (3, "Half Hour"))
    common_date = models.ForeignKey(CommonDate)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    period = models.IntegerField()
    is_available = models.BooleanField()
    priority = models.IntegerField()
    duration_discreteness = models.IntegerField(choices=DURATION, default=1)


class Order(models.Model):
    order_id = models.IntegerField()
#    client_id =


class OrderProduct(models.Model):
    order = models.ForeignKey(Order)


class DesiredDate(CommonDate):
    order_product = models.ForeignKey(OrderProduct)


class ReservedDate(CommonDate):
    order_product = models.ForeignKey(OrderProduct)
    name_of_reserv = models.TextField()


class AvailableDate(CommonDate):
    pass


class Language(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=4)

    def __unicode__(self):
        return u'%s' % (self.name)


#class Info(ClientAwareModel):
class Info(models.Model):
    def get_info_property(self, property_name):
        lang = get_language()
        translation = self.translation_set.filter(lang__code=lang[:2])
        if translation.count():
            return getattr(translation[0], property_name)
        return ('No translation')

    @property
    def title(self):
        return self.get_info_property('title')

    @property
    def short_description(self):
        return self.get_info_property('short_description')

    @property
    def description(self):
        return self.get_info_property('description')

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


def resize_uploaded_image(initial_image, max_size):
    thumb_file = initial_image
    parser = ImageFile.Parser()
    thumb_file.seek(0)
    portion = thumb_file.read(PORTION_SIZE)
    while portion:
        parser.feed(portion)
        portion = thumb_file.read(PORTION_SIZE)
    image_file = parser.close()
    size = image_file.size
    ratio = max([i / float(max_size) for i in size])
    resized_image = image_file.resize([int(i / ratio) for i in size])
    thumb = StringIO()
    resized_image.save(thumb, image_file.format)
    return InMemoryUploadedFile(thumb, "field_name",
                                thumb_file.name, thumb_file.content_type,
                                thumb.len, thumb_file.charset)


@receiver(pre_save, sender=InfoImage)
def resize_image_handler(sender, instance=None, **kwargs):
#    import ipdb; ipdb.set_trace()
    if isinstance(instance.thumbnail.file, UploadedFile):
        instance.thumbnail = resize_uploaded_image(instance.thumbnail.file,
                                                    320)
    if isinstance(instance.image.file, UploadedFile):
        instance.image = resize_uploaded_image(instance.image.file, 800)


#class ConsumerFeedback(ClientAwareModel):
class ConsumerFeedback(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    name = models.CharField(max_length=100)
    e_mail = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.title)


#class Tare(ClientAwareModel):
class Tare(models.Model):
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
    order_product = models.ForeignKey(OrderProduct)
    available_date = models.ManyToManyField(AvailableDate)


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
    short_description = models.TextField()
    description = models.TextField()
    lang = models.ForeignKey(Language)


class News(Info):
    date = models.DateField()

    class Meta:
        ordering = ('-date',)


class AddressType(models.Model):
    name = models.CharField('Type of address', max_length=250)

    def __unicode__(self):
        return u'%s' % (self.name)


#class Address(ClientAwareModel):
class Address(models.Model):
    address_type = models.ForeignKey(AddressType)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    e_mail = models.EmailField()

    def get_address_property(self, property_name):
        lang = get_language()
        translation = self.addresstranslation_set.filter(lang__code=lang[:2])
        if translation.count():
            return getattr(translation[0], property_name)
        return ('No translation')

    @property
    def address(self):
        return self.get_address_property('address_text')

    def __unicode__(self):
        return u'%s (%s)' % (self.address, self.address_type)


class AddressTranslation(models.Model):
    address = models.ForeignKey(Address)
    address_text = models.TextField('Address')
    lang = models.ForeignKey(Language)
