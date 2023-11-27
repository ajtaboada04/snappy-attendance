from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
import datetime

# Create your models here.

class SessionManager(models.Manager):
    def create_new_session(self, course, date):
        # Calculate the next session number
        last_session = Session.objects.filter(course=course).order_by('session_number').last()
        next_session_number = last_session.session_number + 1 if last_session else 1

        # Create the new session
        session = self.create(course=course, date=date, session_number=next_session_number)
        return session

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
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('late', 'Late'), ('absent', 'Absent')], default='absent')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
    
class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_number = models.IntegerField(default=1)
    attendance_records = models.ManyToManyField(Attendance, related_name='sessions')
    date = models.DateField(default=datetime.date.today)
    
    objects = SessionManager()

    def __str__(self):
        string_parts = [f"Session: {self.date} - {self.course.course_name}"]

        # Iterate over related attendance records
        for record in self.attendance_records.all():
            string_parts.append(f"{record.student.name} - {record.date} - {record.status}")

        return '\n'.join(string_parts)