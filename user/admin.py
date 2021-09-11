from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserAdmin(UserAdmin):
    list_filter = ('is_leader','is_guild_member',)
    list_display = ['email', 'discord', 'nickname', 'dkp_balance',
                    'is_leader', 'is_guild_member',
                    ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (None, {
            'classes': ('wide',),
            'fields': ('discord', 'nickname', 'dkp_balance', 'is_leader', 'is_guild_member',),
        }),
    )
    class Meta:
        model = User

admin.site.register(User, UserAdmin)




