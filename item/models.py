from django.db import models
from pytils.translit import slugify


class ItemSubCategory(models.Model):
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название(оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    internal_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name_en)
        super(ItemSubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_en}'


class ItemCategory(models.Model):
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    subcategories = models.ManyToManyField(ItemSubCategory,blank=True,verbose_name='Податегории')
    name_en = models.CharField('Название(оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    internal_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name_en)
        super(ItemCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_en}'





class PerkType(models.Model):
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название(оригинал)', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    internal_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name_en)
        super(PerkType, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_en}'



class Perk(models.Model):
    type = models.ForeignKey(PerkType, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Тип перка ', db_index=True)
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    internal_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=True)
    name_en = models.CharField('Название(оригинал)', max_length=255, blank=True, null=True, db_index=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    icon = models.ImageField('Изображение', upload_to='images/items/perk/', blank=True)

    description = models.CharField('Описание', max_length=255, blank=True, null=True)
    description_en = models.CharField('Описание (оригинал)', max_length=255, blank=True, null=True)

    tier = models.IntegerField(db_index=True, blank=True, null=True)
    rarity = models.IntegerField(db_index=True, blank=True, null=True)
    fishRarityRollModifier = models.IntegerField(db_index=True, blank=True, null=True)
    fishSizeRollModifier = models.IntegerField(db_index=True, blank=True, null=True)

    dayPhases = models.CharField(max_length=255, blank=True, null=True)
    fishingWaterType = models.CharField(max_length=255, blank=True, null=True)
    is_perk_with_attributes = models.BooleanField(default=False)

    scalingPerGearScore = models.DecimalField(max_digits=21,decimal_places=20,blank=True,null=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name_en)
        super(Perk, self).save(*args, **kwargs)

    def __str__(self):
        if self.name_en:
            return f'{self.name_en}'
        else:
            return self.internal_id

class PerkAttribute(models.Model):
    perk = models.ForeignKey(Perk, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Перк',related_name='perk_attributes')
    attribute = models.CharField(max_length=10, blank=True, null=True)
    value = models.DecimalField(max_digits=3,decimal_places=2,blank=True,null=True)
    values = models.CharField(max_length=20, blank=True, null=True)

class Item(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Категория ', db_index=True)
    subcategory = models.ForeignKey(ItemSubCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Подкатегория ', db_index=True)
    internal_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=True)
    icon_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=True)
    name = models.CharField('Название предмета', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название предмета(оригинал)', max_length=255, blank=True, null=True, db_index=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    icon = models.ImageField('Иконка', upload_to='images/items/icons/', blank=True)
    image = models.ImageField('Изображение', upload_to='images/items/full/', blank=True)

    description = models.CharField('Описание предмета',max_length=255, blank=True, null=True)
    description_en = models.CharField('Описание предмета (оригинал)',max_length=255, blank=True, null=True)

    tier = models.IntegerField(blank=True, null=True, db_index=True)
    rarity = models.IntegerField(blank=True, null=True, db_index=True)

    baseDamage = models.IntegerField(blank=True, null=True)
    gearScore = models.IntegerField(blank=True, null=True, db_index=True)
    gearScoreMin = models.IntegerField(blank=True, null=True, db_index=True)
    gearScoreMax = models.IntegerField(blank=True, null=True, db_index=True)

    weight = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    bindOnPickup = models.BooleanField(default=False)
    bindOnEquip = models.BooleanField(default=False)
    namedItem = models.BooleanField(default=False)

    durability = models.IntegerField(blank=True, null=True)
    staggerDamage = models.IntegerField(blank=True, null=True)

    critChance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    critDamageMultiplier = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    blockStaminaDamage = models.CharField(max_length=255, blank=True, null=True)
    blockStability = models.CharField(max_length=255, blank=True, null=True)
    weightClass = models.CharField(max_length=255, blank=True, null=True)



    can_be_crafted = models.BooleanField(default=False)
    quest_reward = models.BooleanField(default=False)
    hasRandomPerks = models.BooleanField(default=False)

    perks = models.ManyToManyField(Perk, blank=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_en}'


class ItemAttributeScale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Предмет',related_name='scale_attributes')
    attribute = models.CharField(max_length=10, blank=True, null=True)
    value = models.DecimalField(max_digits=5,decimal_places=4,blank=True,null=True)




