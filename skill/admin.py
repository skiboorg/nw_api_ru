from django.contrib import admin

from .models import *

class SkillInline (admin.TabularInline):
    exclude = ['image','name','row','col','parent_skill',]
    model = Skill
    extra = 0

class FeedbackInline (admin.TabularInline):
    model = BuildFeedback
    extra = 0

class SkillAdmin(admin.ModelAdmin):

    list_filter = ('tree',)
    class Meta:
        model = Skill

class BuildAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','is_private']
    list_filter = ('is_active','is_private',)
    inlines = [FeedbackInline]
    class Meta:
        model = Build

class SkillTreeAdmin(admin.ModelAdmin):
    inlines = [SkillInline]

    class Meta:
        model = SkillTree

admin.site.register(Weapon)
admin.site.register(Skill,SkillAdmin)
admin.site.register(SkillTree,SkillTreeAdmin)
admin.site.register(Build,BuildAdmin)
admin.site.register(Characteristic)

