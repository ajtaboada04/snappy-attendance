from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
import datetime

# Create your models here.

from django.contrib.auth.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=255, validators=[MinLengthValidator(2, "Course name must be greater than 2 characters")])
    semester = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.course_name

class Professor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2, "Name must be greater than 2 characters")])
    courses = models.ManyToManyField(Course, related_name='professors')

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2, "Name must be greater than 2 characters")])
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.name
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('late', 'Late'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attendance_records = models.ManyToManyField(Attendance, related_name='sessions')

    def __str__(self):
        return f"Session for {self.course.course_name}"

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attendance_records = models.ManyToManyField(Attendance, related_name='classes')

    def __str__(self):
        return f"Class of {self.course.course_name}"