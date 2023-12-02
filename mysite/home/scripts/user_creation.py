import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
django.setup()

from django.contrib.auth.models import User
from your_app.models import Professor, Student, Course

# Function to create user and assign role-specific profile
def create_user(username, email, password, role, name, courses):
    # Create User
    user = User.objects.create_user(username=username, email=email, password=password)

    # Create role-specific profile and assign courses
    if role.lower() == 'professor':
        professor = Professor.objects.create(user=user, name=name)
        for course_name in courses:
            course, created = Course.objects.get_or_create(course_name=course_name)
            professor.courses.add(course)
    elif role.lower() == 'student':
        student = Student.objects.create(user=user, name=name)
        for course_name in courses:
            course, _ = Course.objects.get_or_create(course_name=course_name)
            student.courses.add(course)
            
courses = ['Designing and Using Databases', 'Programming 1', 'Algorithms & Data Structures', 'Cloud Computing', 'Technology', 'Calculus for Computer Science']
            
students = [('ricardo', 'rmendez.ieu2022@student.ie.edu', 'password123', 'student', 'Ricardo Mendez', courses),
            ]
professors = [('antonio', 'amomblan@ie.edu', 'password123', 'professor', 'Antonio Momblan', [courses[2]]),
              ]

# Create users
for student in students:
    create_user(*student)

for professor in professors:
    create_user(*professor)
