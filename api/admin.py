from django.contrib import admin
from .models import *

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id','created_at','is_viewed']

    list_filter = ('is_viewed',)
    class Meta:
        model = Feedback

admin.site.register(Texts)
admin.site.register(Banner)
admin.site.register(Faq)
admin.site.register(SocialItem)
admin.site.register(Feedback,FeedbackAdmin)