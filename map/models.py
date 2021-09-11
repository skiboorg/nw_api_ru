from django.db import models
from pytils.translit import slugify
from colorfield.fields import ColorField

class Poi(models.Model):
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название(оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    description = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description_en = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    image = models.ImageField('Изображение', upload_to='poi/', blank=True)
    level = models.CharField(max_length=255, blank=True, null=True)

    lat = models.DecimalField(blank=True, null=True,decimal_places=8,max_digits=15)
    lng = models.DecimalField(blank=True, null=True,decimal_places=8,max_digits=15)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name_en)
        super(Poi, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} | {self.name_en} | {self.description}'



class ResourceCategory(models.Model):

    name = models.CharField('Категория ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Категория (оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение', upload_to='images/resource/', blank=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} | {self.name_en} '

    class Meta:
        ordering = ['name_en']

class Resource(models.Model):
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Тип',related_name='resourses')
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description_en = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    level = models.CharField(max_length=255,blank=True, null=True)

    lat = models.DecimalField(blank=True, null=True,decimal_places=8,max_digits=15)
    lng = models.DecimalField(blank=True, null=True,decimal_places=8,max_digits=15)


class ResourceType(models.Model):
    name = models.CharField('Категория ', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    category = models.ManyToManyField(ResourceCategory, blank=True)
    is_visible = models.BooleanField(default=False)
    marker_color = ColorField('Цвет', default='#000000')
    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(ResourceType, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'