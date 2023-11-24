from django.contrib import admin
from .models import Professor, Student, Course

admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Course)