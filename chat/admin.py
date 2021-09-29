from django.contrib import admin
from . models import*

# Register your models here.

admin.site.register(Chat_User)
admin.site.register(Messages)
admin.site.register(Room)
admin.site.register(Participants)
admin.site.register(Message)
