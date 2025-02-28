from django.contrib import admin

# Register your models here.
from .models import TwitchPost
from .models import Profile
from .models import Follow
admin.site.register(TwitchPost)
admin.site.register(Profile)
admin.site.register(Follow)