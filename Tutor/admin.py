from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Hire)
admin.site.register(Employ)
admin.site.register(AskEmploy)
admin.site.register(Exp)
admin.site.register(EmployRelationship)
