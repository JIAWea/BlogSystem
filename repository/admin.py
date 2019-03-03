from django.contrib import admin
from repository.models import *

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Article2Tag)
admin.site.register(User2User)
