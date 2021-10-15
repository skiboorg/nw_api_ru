from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django_random_queryset import RandomManager

class Banner(models.Model):
    order = models.IntegerField(default=10)
    top_text = models.CharField(max_length=255, blank=True, null=True)
    bottom_text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='images/banner/', blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    is_url_for_site = models.BooleanField('cссылка с баннера на другой сайт?', default=False)

    class Meta:
        ordering = ('order',)


class Faq(models.Model):
    order = models.IntegerField(default=100)
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)


class SocialItem(models.Model):
    order = models.IntegerField(default=100)
    logo = models.ImageField( upload_to='images/social/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url_youtube = models.CharField('Ссылка ютуб',max_length=255, blank=True, null=True)
    url_twitch = models.CharField('Ссылка твич',max_length=255, blank=True, null=True)

    objects = RandomManager()

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.order} | {self.name}'

class Feedback(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    is_viewed = models.BooleanField(default=False)

class Texts(models.Model):
    about_text = RichTextUploadingField(blank=True, null=True)
    policy_text = RichTextUploadingField(blank=True, null=True)