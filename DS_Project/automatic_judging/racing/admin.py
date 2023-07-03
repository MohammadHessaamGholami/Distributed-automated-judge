from django.contrib import admin

# Register your models here.

from racing.models import Racing, Question, StudentRacing, StudentQuestion

admin.site.register(Racing)
admin.site.register(Question)
admin.site.register(StudentRacing)
admin.site.register(StudentQuestion)