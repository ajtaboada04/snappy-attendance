import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth.models import User
from home.models import Professor, Student, Course

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
            
courses = ['Algorithms and Data Structures', 'Calculus for Computer Science', 'Cloud Computing', 'Computer Programming 1',
           'Designing and Using Databases', 'Technology']
            
students = [('ricardo', 'rmendez.ieu2022@student.ie.edu', 'password123', 'student', 'Ricardo Andres Mendez Cavalieri', courses),
            ('andres', 'ataboada.ieu2022@student.ie.edu', 'password123', 'student', 'Andres Jose Taboada Santamaria', courses),
            ('saleh', 'sabdelrahman.ieu2022@student.ie.edu', 'password123', 'student', 'Saleh Hassan Ibrahim Hassan Abd Elrahman', courses),
            ('david', 'dadeakin.ieu2022@student.ie.edu', 'password123', 'student', 'David Oreoluwa Ayomide Adeakin', courses),
            ('zaidkhaled', 'zalsaheb.ieu2022@student.ie.edu', 'password123', 'student', 'Zaid Khaled Alsaheb', courses),
            ('zaidsaad', 'zaltayan.ieu2022@student.ie.edu', 'password123', 'student', 'Zaid Saad Nadeem Al Tayan', courses),
            ('andrei', 'abaraitaru.ieu2022@student.ie.edu', 'password123', 'student', 'Andrei Baraitaru', courses),
            ('shayan', 'sborhani.ieu2023@student.ie.edu', 'password123', 'student', 'Shayan Borhani', courses),
            ('leonardo', 'lcamilleri.ieu2022@student.ie.edu', 'password123', 'student', 'Leonardo Camilleri', courses),
            ('laura', 'lcuellar.ieu2022@student.ie.edu', 'password123', 'student', 'Laura Patricia Cuellar Camacho', courses),
            ('luis', 'lgomezacebo.ieu2022@student.ie.edu', 'password123', 'student', 'Luis Gomez-Acebo Martin-Retorillo', courses),
            ('joseantonio', 'jizarra.ieu2022@student.ie.edu', 'password123', 'student', 'Jose Antonio Izarra Millan', courses),
            ('peter', 'pkaracs.ieu2022@student.ie.edu', 'password123', 'student', 'Peter Norbert Karacs', courses),
            ('alexandra', 'akhreiche.ieu2022@student.ie.edu', 'password123', 'student', 'Alexandra Khreiche', courses),
            ('nicolas', 'nleyva.ieu2022@student.ie.edu', 'password123', 'student', 'Nicolas Leyva Gonzalez', courses),
            ('angel', 'alopez.ieu2022@student.ie.edu', 'password123', 'student', 'Angel Lopez Torralba', courses),
            ('guy', 'gmazar.ieu2022@student.ie.edu', 'password123', 'student', 'Guy Mazar', courses),
            ('jocelyn', 'jmin.exstudents2023@student.ie.edu', 'password123', 'student', 'Jocelyn Xin Yi Min', courses),
            ('karl', 'kmouchantaf.ieu2022@student.ie.edu', 'password123', 'student', 'Karl Mouchantaf', courses),
            ('clara', 'cmouzannar.ieu2022@student.ie.edu', 'password123', 'student', 'Clara Mouzannar', courses),
            ('agustin', 'amuller.ieu2021@student.ie.edu', 'password123', 'student', 'Agustin Patrice Michel Ludovi Muller', courses),
            ('jafar', 'jobeidat.ieu2022@student.ie.edu', 'password123', 'student', 'Jafar Mohammed Ahmad Obeidat', courses),
            ('farah', 'forfaly.ieu2022@student.ie.edu', 'password123', 'student', 'Farah Orfaly', courses),
            ('sebastian', 'sperilla.ieu2021@student.ie.edu', 'password123', 'student', 'Sebastian Perilla Espinosa', courses),
            ('julius', 'jpfin.exstudents2023@student.ie.edu', 'password123', 'student', 'Julius Pfingsten', courses),
            ('ismael', 'ipicazo.ieu2022@student.ie.edu', 'password123', 'student', 'Ismael Picazo Flores', courses),
            ('massimo', 'mridella.ieu2022@student.ie.edu', 'password123', 'student', 'Massimo Giuseppe Ridella', courses),
            ('pietro', 'prodrigano.ieu2022@student.ie.edu', 'password123', 'student', 'Pietro Rodrigano Abril', courses),
            ('rodrigo', 'rsagastegui.ieu2022@student.ie.edu', 'password123', 'student', 'Rodrigo Jesus Sagastegui Martinez', courses),
            ('daniel', 'dsanchez.ieu2022@student.ie.edu', 'password123', 'student', 'Daniel Marcos Sanchez Velilla', courses),
            ('josemiguel', 'jserrano.ieu2022@student.ie.edu', 'password123', 'student', 'Jose Miguel Serrano Flores', courses),
            ('anna', 'ashats.ieu2022@student.ie.edu', 'password123', 'student', 'Anna Shats', courses),
            ('els', 'evaks.ieu2022@student.ie.edu', 'password123', 'student', 'Els Aleksandra Vaks', courses),
            ('noah', 'nvalderrama.ieu2022@student.ie.edu', 'password123', 'student', 'Noah Valderrama Hernando', courses),
            ('jorge', 'jvargas.ieu2022@student.ie.edu', 'password123', 'student', 'Jorge Vargas Timon', courses),
            ('sofia', 'svitorica.ieu2022@student.ie.edu', 'password123', 'student', 'Sofia Vitorica Nogues', courses),
            ('edouard', 'ewidmaierrui.ieu2022@student.ie.edu', 'password123', 'student', 'Edouard Widmaier-Ruiz-Picasso', courses),
            ('luismarc', 'lwoerner.ieu2023@student.ie.edu', 'password123', 'student', 'Luis Marc Josef Woerner', courses),
            ('paul', 'pzwir.exstudents2023@student.ie.edu', 'password123', 'student', 'Paul Zwirner', courses),
            ('arian', 'ahani.exstudents2023@student.ie.edu', 'password123', 'student', 'Arian Hanifi', courses),
            ('francisco', 'fmago.exstudents2023@student.ie.edu', 'password123', 'student', 'Francisco Javier Magot Barrera', courses),
            ('claire', 'cmahon.ieu2023@student.ie.edu', 'password123', 'student', 'Claire McMahon', courses)]

professors = [('antonio', 'amomblan@ie.edu', 'password123', 'professor', 'Antonio Momblan', [courses[0]]),
              ('gokce', 'gdeliorman@faculty.ie.edu', 'password123', 'professor', 'Gokce Deliorman', [courses[1]]),
              ('eduardo', 'erodriguezl@faculty.ie.edu', 'password123', 'professor', 'Eduardo Rodriguez-Lopez', [courses[2], courses[4]]),
              ('suzan', 'suzant@faculty.ie.edu', 'password123', 'professor', 'Suzan Awainat', [courses[3]]),
              ('pierre', 'pauger@faculty.ie.edu', 'password123', 'professor', 'Pierre Auger', [courses[5]])]

# Create users
for student in students:
    create_user(*student)

for professor in professors:
    create_user(*professor)
