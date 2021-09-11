from django.db import models
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField

def humanize_time(time):
    from django.utils.timesince import timesince
    return timesince(time)

class Weapon(models.Model):
    order = models.IntegerField(default=50)
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название (оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    main_char = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='images/weapon/', blank=True)
    description = models.TextField(blank=True, null=True)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order} | {self.name}'

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Weapon, self).save(*args, **kwargs)

    class Meta:
        ordering = ['order']


class SkillTree(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Оружие', related_name='trees')
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название (оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    description = models.TextField(blank=True, null=True)
    spent_points = models.IntegerField(default=0)
    checked_skills = models.JSONField(blank=True,null=True)

    def __str__(self):
        return f'{self.name} | {self.name_en}'


class Skill(models.Model):
    tree = models.ForeignKey(SkillTree, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Ветка', related_name='skills')
    parent_skill = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Родитель')
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название (оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    image = models.ImageField('Иконка', upload_to='images/skill/', blank=True)
    description = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    is_parent = models.BooleanField(default=False)
    is_has_parent = models.BooleanField(default=False)
    is_active_skill = models.BooleanField(default=False)
    is_ultimate = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    is_can_check = models.BooleanField(default=False)
    is_empty = models.BooleanField(default=False)
    is_has_left_parent = models.BooleanField(default=False)
    row = models.IntegerField('Ряд', default=1)
    col = models.IntegerField('Колонка', default=1)

    def __str__(self):
        return f'{self.name_en} | {self.name} | R: {self.row} C:{self.col}'

    class Meta:
        ordering = ['name_en']


class Build(models.Model):
    weapon1 = models.ForeignKey(Weapon, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Оружие',related_name='weapon1')
    weapon2 = models.ForeignKey(Weapon, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Оружие',related_name='weapon2')
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    purpose = models.CharField('Предназначение ', max_length=255, blank=True, null=True)
    role = models.CharField('Роль ', max_length=255, blank=True, default='Не указана')
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    checked_skills_left_w1 = models.JSONField(blank=True,null=True)
    checked_skills_right_w1 = models.JSONField(blank=True,null=True)
    checked_skills_left_w2 = models.JSONField(blank=True, null=True)
    checked_skills_right_w2 = models.JSONField(blank=True, null=True)
    characteristics = models.JSONField(blank=True, null=True)
    total_rating = models.IntegerField('Рейтинг Всего', default=0)
    rating = models.IntegerField('Рейтинг', default=0)
    votes = models.IntegerField('Голосов', default=0)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.votes > 0:
            self.rating = self.total_rating / self.votes
        super(Build, self).save(*args, **kwargs)

    def get_humanize_time(self):
        return humanize_time(self.created_at)

    class Meta:
        ordering = ['-rating','-created_at']


class Characteristic(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    name_en = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    min = models.IntegerField(default=5)
    max = models.IntegerField(default=300)
    step1_description = RichTextUploadingField(blank=True, null=True)
    step1_val = models.IntegerField(default=50)
    step2_description = RichTextUploadingField(blank=True, null=True)
    step2_val = models.IntegerField(default=100)
    step3_description = RichTextUploadingField(blank=True, null=True)
    step3_val = models.IntegerField(default=150)
    step4_description = RichTextUploadingField(blank=True, null=True)
    step4_val = models.IntegerField(default=200)
    step5_description = RichTextUploadingField(blank=True, null=True)
    step5_val = models.IntegerField(default=250)
    step6_description = RichTextUploadingField(blank=True, null=True)
    step6_val = models.IntegerField(default=300)
    current_val = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.name}'

class BuildFeedback(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Билд',related_name='feedbacks')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Юзер')
    value = models.IntegerField(default=0)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)