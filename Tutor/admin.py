from django.contrib import admin
from .models import Parent,Tutor,Subject,PTMessage,TPMessage,PTComment,TPComment,Employ
# Register your models here.
admin.site.register(Parent)
admin.site.register(Tutor)
admin.site.register(Subject)
admin.site.register(PTMessage)
admin.site.register(TPMessage)
admin.site.register(PTComment)
admin.site.register(TPComment)
admin.site.register(Employ)
