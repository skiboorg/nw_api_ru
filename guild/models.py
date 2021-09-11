from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify


class Guild(models.Model):
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    fraction = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    server = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    style = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    size = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    image = models.ImageField('Изображение', upload_to='images/guild/', blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    discord_link = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    votes_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    total_rating = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.fraction} '

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        if self.votes_count > 0:
            self.total_rating = self.rating / self.votes_count
        super(Guild, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-rating']


class GuildFeedback(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE,null=True,blank=False)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE,null=True,blank=False,related_name='feedbacks')
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.is_active:
            self.guild.rating += self.rating
            self.guild.votes_count += 1
            self.guild.save()
        super(GuildFeedback, self).save(*args, **kwargs)