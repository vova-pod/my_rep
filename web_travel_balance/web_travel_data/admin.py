from django.contrib import admin

from .models import Member, Contribution, Expence, Exeption


admin.site.register(Member)
admin.site.register(Contribution)
admin.site.register(Expence)
admin.site.register(Exeption)
