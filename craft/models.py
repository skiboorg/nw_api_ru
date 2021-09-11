from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify


class Category(models.Model):
    order = models.IntegerField(default=100)
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название англ', max_length=255, blank=True, null=True)
    name_slug = models.CharField('Название ', max_length=255, blank=True, null=True,editable=False)
    image = models.ImageField('Изображение', upload_to='images/craft/', blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    description_en = RichTextUploadingField(blank=True, null=True)



    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    # class Meta:
    #     ordering = ['order','-created_at']


class Item(models.Model):
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название англ', max_length=255, blank=True, null=True)
    name_slug = models.CharField('Название ', max_length=255, blank=True, null=True, editable=False)
    image = models.ImageField('Изображение', upload_to='images/craft/', blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    description_en = RichTextUploadingField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    # class Meta:
    #     ordering = ['order','-created_at']

class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Категория',related_name='recipes')
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_en = models.CharField('Название англ', max_length=255, blank=True, null=True)
    name_slug = models.CharField('Название ', max_length=255, blank=True, null=True, editable=False)
    image = models.ImageField('Изображение', upload_to='images/craft/', blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    description_en = RichTextUploadingField(blank=True, null=True)
    exp = models.IntegerField('Опыт', default=0)
    weight = models.DecimalField('Вес', decimal_places=2, max_digits=4, default=0)

    def __str__(self):
        return f'Рецепт : {self.name}'

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

class RecipeItem(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Рецепт',related_name='items')
    item = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True,verbose_name='Ингридиент')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Ингридиент рецепта f{self.recipe.name}'

class RecipeRecipe(models.Model):
    main_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Рецепт',related_name='main_recipe')
    recipe_item = models.ForeignKey(Recipe,on_delete=models.CASCADE,blank=True,null=True,verbose_name='Ингридиент Рецепт',related_name='recipe_items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Ингридиент Рецепт рецепта f{self.main_recipe.name}'
