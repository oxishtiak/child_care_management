from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Staff)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(Package)