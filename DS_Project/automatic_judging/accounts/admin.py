from django.contrib import admin

# Register your models here.

from accounts.models import User, Teacher, Student

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)