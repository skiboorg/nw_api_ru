from django.contrib import admin
from .models import *


class ItemAttributeScaleInline (admin.TabularInline):
    model = ItemAttributeScale
    extra = 0



class ItemAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ItemAttributeScaleInline]
    list_filter = ('category','subcategory',)
    class Meta:
        model = Item

class PerkAttrubuteInline (admin.TabularInline):
    model = PerkAttribute
    extra = 0

class PerkAdmin(admin.ModelAdmin):
    # list_display = ['name']
    inlines = [PerkAttrubuteInline]
    list_filter = ('type',)
    class Meta:
        model = Perk


admin.site.register(Item,ItemAdmin)
admin.site.register(ItemCategory)
admin.site.register(ItemSubCategory)
admin.site.register(Perk, PerkAdmin)
admin.site.register(PerkAttribute)