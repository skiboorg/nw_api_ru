from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify


class PostItem(models.Model):
    order = models.IntegerField(default=100)
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Изображение', upload_to='images/post/', blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(PostItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order} | {self.name}'

    class Meta:
        ordering = ['-created_at']
