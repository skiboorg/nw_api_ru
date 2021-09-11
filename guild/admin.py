from django.contrib import admin
from .models import *

class FeedbackInline (admin.TabularInline):
    model = GuildFeedback
    extra = 0


class GuildAdmin(admin.ModelAdmin):
    list_display = ['name','is_active']
    inlines = [FeedbackInline]
    list_filter = ('is_active',)
    class Meta:
        model = Guild

class GuildFeedbackAdmin(admin.ModelAdmin):
    list_display = ['created_at','is_active']
    list_filter = ('is_active',)
    class Meta:
        model = GuildFeedback


admin.site.register(Guild,GuildAdmin)
admin.site.register(GuildFeedback,GuildFeedbackAdmin)