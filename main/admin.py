from django.contrib import admin

# Register your models here.
from main.models import *

admin.site.register(Staff)
admin.site.register(TgUser)
admin.site.register(Offer)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Poll)
admin.site.register(PollResult)
admin.site.register(Photos)
