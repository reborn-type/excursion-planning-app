from django.contrib import admin
from .models import Route, Excursion, UserProfile, Group
# Register your models here.

admin.site.register(Route)
admin.site.register(Excursion)
admin.site.register(UserProfile)
admin.site.register(Group)