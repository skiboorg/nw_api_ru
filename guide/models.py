from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify


class GuideCategory(models.Model):
    order = models.IntegerField(default=100)
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(GuideCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'№ПП{self.order} | {self.name}'

    class Meta:
        ordering = ['order']


class Guide(models.Model):
    category = models.ForeignKey(GuideCategory,on_delete=models.CASCADE,null=True, blank=False , related_name='guides')
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение', upload_to='images/guide/', blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    views = models.IntegerField(default=0)
    video_link = models.CharField(max_length=255, blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    is_video = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_video:
            return f'{self.id} | Видео гайд | {self.category.name}  '
        else:
            return f'Гайд | {self.name} | {self.category.name}'

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Guide, self).save(*args, **kwargs)

