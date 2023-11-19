from django.db import models

# Create your models here.

class Accounts(models.Model): # models.Model -> inheritance
    account_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=255) 
    email = models.EmailField()  
    university_email = models.EmailField()  
    password = models.CharField(max_length=255)  
    # Defining choices for the role field using Django's choices option
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)  
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)



class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)  
    course_name = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)



class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)  
    class_name = models.CharField(max_length=255)



class Students(models.Model):
    student_id = models.AutoField(primary_key=True)  
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)



class Courses_to_Professor(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)



class Classes_to_Courses(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)



class Session(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    session_id = models.AutoField(primary_key=True)  



class Attendance(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
