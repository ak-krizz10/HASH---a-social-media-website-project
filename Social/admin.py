from django.contrib import admin
from .models import *

# Register your models here.



admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Reply)
admin.site.register(ScreenTime)
admin.site.register(Notification)