from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link professor account to a respective user
    name = models.CharField(max_length=255)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link professor account to a respective user  

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    students = models.ManyToManyField(Student)
    professors = models.ManyToManyField(Professor)
    
class Attendance(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Session(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    attendance = models.OneToOneField(Attendance, on_delete=models.CASCADE)
    
class Class(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)