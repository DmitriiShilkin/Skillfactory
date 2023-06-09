from django.contrib import admin

from .models import Passage, Coords, Level, Images, Areas, User

# Register your models here.
admin.site.register(Passage)
admin.site.register(Coords)
admin.site.register(Level)
admin.site.register(Images)
admin.site.register(Areas)
admin.site.register(User)
