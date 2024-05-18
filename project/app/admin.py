from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(YouTuber)
# admin.site.register(Tag)
admin.site.register(Posts)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Subscription)
admin.site.register(Blocked_Subscriber)