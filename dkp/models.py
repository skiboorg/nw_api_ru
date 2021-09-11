from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify


class Event(models.Model):
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    creator = models.ForeignKey('user.User',on_delete=models.CASCADE,
                                blank=True,null=True,verbose_name='Создатель',related_name='creator')

    date = models.DateField('Дата', blank=True, null=True)
    time = models.TimeField('Время', blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    dpk_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    players_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-is_active',)


class EventDkp(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,
                                blank=True,null=True,verbose_name='Событие',related_name='players')
    player = models.ForeignKey('user.User', on_delete=models.CASCADE,
                                blank=True, null=True, verbose_name='Игрок')
    amount = models.IntegerField(default=0)



class TradeItem(models.Model):
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    price = models.IntegerField(default=0)

class Trade(models.Model):
    item = models.ForeignKey(TradeItem,on_delete=models.CASCADE,
                                blank=True,null=True,verbose_name='Лот')
    item_count = models.IntegerField(default=0)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    hours = models.IntegerField(default=0)
    add_time = models.IntegerField(default=0)
    start_price = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    last_bid = models.DateTimeField(blank=True, null=True)


    def save(self, *args, **kwargs):
        self.start_price = self.item_count * self.item.price
        super(Trade, self).save(*args, **kwargs)

class TradePlayer(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE,
                              blank=True, null=True, verbose_name='Событие')
    player = models.ForeignKey('user.User', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Игрок', related_name='players')
    last_bid = models.IntegerField(default=0)