from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Activation
from twitter.models import Twitter
from django.contrib.auth.models import User


class TwitterInline(admin.StackedInline):
    model = Twitter
    can_delete = False
    verbose_name_plural = 'Twitter'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (TwitterInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Activation)