import requests

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
from django.http import JsonResponse
from django.conf import settings


from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect



from .models import Student, Professor, Course, Session, Attendance

# VIEWS: Logic of the application

# HomeView: renders the home page
class HomeView(View):
    
    # HTML template rendered when the page is opened
    template_name = "home/main.html"
    # Method triggered when a GET request hits the url
    # associated with HomeView
    def get(self, request):
        
        context = {}
        
        #Default role of any user accessing the view
        role = "user"
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            
            # Query the user type related to the user and setting
            # the role respectively
            if Student.objects.filter(user=request.user).exists():
                role = "student"
            elif Professor.objects.filter(user=request.user).exists():
                role = "professor"
                
        context["role"] = role
        
        # render the HTML with the given template and passing
        # the role as context
        return render(request, self.template_name, context)

#StudentDashboardView: renders the student dashboard page
#LoginRequiredMixin is used to only allow authenticated users
#to access this view
class StudentDashboardView(LoginRequiredMixin, View):
    
    # HTML template rendered when the page is opened
    template_name = 'home/student_dashboard.html'
    
    # Method triggered when a GET request hits the url
    # associated with StudentDashboardView
    def get(self, request):
        context = {}
        
        # If user is authenticated, query his Student object and
        # his classes
        if request.user.is_authenticated:
            student = get_object_or_404(Student, user = request.user)
            classes = student.courses.all()
            context['classes'] = classes
            context['student'] = student
        
        # Renders page with the given template and
        # the student and his classes as context
        return render(request, self.template_name, context)

    # Method triggered when a POST request hits the view
    # this happens when the student submits an attendance code
    def post(self, request):
        
        # Get the code and class_id from the POST request
        selected_class_id = request.POST.get('selected_class')
        attendance_code = request.POST.get('attendance_code')
        
        # Query the database to get the student and the course
        # if not found, view returns a 404
        student = get_object_or_404(Student, user=request.user)
        course = get_object_or_404(Course, id=selected_class_id)
        
        
        # Write the class_id into the user's session
        request.session["selected_class_id"] = selected_class_id

        # URL of your Azure Function (taken from the environment)
        
        azure_function_url = f"{settings.VALIDATE_CODE_FUNC}?code={settings.VALIDATE_CODE_KEY}"
        
        # Logic to compare the code given with code in Azure table
        try:
            # Send a post request to Azure with the given code
            # as a JSON payload
            payload = {'code': attendance_code}
            response = requests.post(azure_function_url, json=payload)

            # If the function returns True
            if response.status_code == 200 and response.text == 'true':
                
                # Find the most recent (or current) session number for this course
                latest_session = Session.objects.filter(course=course).aggregate(Max('session_number'))
                session_number = latest_session['session_number__max']

                if session_number is not None:
                    # Get or create the session for the current day with the latest session number
                    session, _ = Session.objects.get_or_create(course=course, session_number=session_number)

                    # Create or update the attendance record
                    attendance_record, created = Attendance.objects.update_or_create(
                    student=student,
                    session=session,
                    defaults={'status': 'present'}
                )
                    
                    return redirect('confirmation')  # Redirect to confirmation view
                else:
                    # Handle the case where no session exists for the course
                    messages.error(request, 'No active session found for this course.')
                    return render(request, self.template_name, {'invalid_code': True, 'student': student, 'classes': student.courses.all()})

            else:
                messages.error(request, 'Invalid attendance code.')
                return render(request, self.template_name, {'invalid_code': True, 'student': student, 'classes': student.courses.all()})

        except requests.RequestException as e:
            messages.error(request, f'Error submitting attendance code: {e}')
            return render(request, self.template_name, {'invalid_code': True, 'student': student, 'classes': student.courses.all()})

# ProfessorDashboardView: renders the professor dashboard only
# if the user is logged in
class ProfessorDashboardView(LoginRequiredMixin, View):
    
    # View's html template
    template_name = 'home/professor_dashboard.html'
    
    # Method triggered when a GET request hits the view
    def get(self, request):
        context = {}
        
        if request.user.is_authenticated:
            
            # Queries the professor and his courses 
            # and returns a 404 if not found and
            # assigns him to the context along with his taught classes
            professor = get_object_or_404(Professor, user=request.user)
            
            classes = professor.courses.all()
            
            context["classes"] = classes
            context["professor"] = professor
        
        # Renders template with the context passed
        return render(request, self.template_name, context)
    
    # Method triggered when a POST request hits the view
    # This happens when the professor begins displayint codes
    def post(self, request):
        
        # Get the selected class by the professor
        # from the POST request
        selected_class_id = request.POST.get('selected_class')
        
        
        try:
            
            # Query database for the course and create the new session
            # Using model method
            today = timezone.now().date()
            selected_class = get_object_or_404(Course, id=selected_class_id)
            new_session = Session.objects.create_new_session(course=selected_class, date=today)
            
            # Add the course and session to the professors' session
            request.session['selected_class_id'] = selected_class_id
            request.session['session_number'] = new_session.session_number
            
        except Course.DoesNotExist:
            request.session['error'] = "Class does not exist."
            
        # Redirect to the view that displays the codes
        return redirect('display_codes')
    
# DisplayCodesView: view that renders the view that displays
# the attendance codes given some logic
class DisplayCodesView(View):
    
    # Template to render
    template_name = 'home/attendance.html'

    # Method triggered when a GET request hits the url
    # related to DisplayCodesView
    def get(self, request):
        context = {}

        # Get the class_id from the session and query the course
        # given such id in the database
        selected_class_id = request.session.get('selected_class_id')
        selected_class = get_object_or_404(Course, id=selected_class_id)
        
        # Query all the students related to the course
        students = Student.objects.filter(courses=selected_class)
        
        # Output the session number to the console for debugging
        print("Session Number:", request.session['session_number'])

        # Assign the course, students and session number to the context
        context["selected_class"] = selected_class
        context["students"] = students
        context["current_session"] = request.session["session_number"]

        # Render the template with the given context
        return render(request, self.template_name, context)

# AttendanceManagementView: view that renders the attendance management
# page for the professor
class AttendanceManagementeView(LoginRequiredMixin, View):
    
    # Template to render
    template_name = "home/attendance_management.html"

    # Method triggered when a GET request hits the url
    def get(self, request):
        
        context = {}
        
        # Get the class_id and session_number from the session
        class_id = request.session.get('selected_class_id')
        session_number = request.session.get('session_number') 

        # Query the database for the course and session
        # given the class_id and session_number
        selected_class = get_object_or_404(Course, id=class_id)
        session = get_object_or_404(Session, course=selected_class, session_number=session_number)

        # Empty list to store the students data
        students_data = []
        
        # Iterate over the student records related to the course
        for student in Student.objects.filter(courses=selected_class):
            
            # Get the first attendance record related to the student and session
            attendance_record = Attendance.objects.filter(student=student, session=session).first()
            
            # Get the status from the record or set it to absent
            status = attendance_record.status if attendance_record else 'absent'
            
            # Append the student data to the list
            students_data.append({
                'id': student.id,
                'name': student.name,
                'status': status,
            })

        # Assign the course, session and students data to the context
        context['selected_class'] = selected_class
        context['current_session'] = session
        context['attendance_records'] = students_data
        
        # Render the template with the given context
        return render(request, self.template_name, context)

    # Method triggered when a POST request hits the url
    def post(self, request):
        print(request.POST)
        context = {}
        
        # Get the class_id and session_number from the session
        class_id = request.session.get('selected_class_id')
        session_number = request.session.get('session_number')
        
        # Query the database for the course and session
        course = get_object_or_404(Course, id=class_id) 
        session = get_object_or_404(Session, course=course, session_number=session_number)

        # Iterate over the students related to the course
        for student in Student.objects.filter(courses=course):
        # Get the status from the form for each student
            status = request.POST.get(f'status_{student.id}', 'absent')
            
            print(status)
            # Update or create the attendance record
            Attendance.objects.update_or_create(
                    student=student,
                    session=session,  # Link the attendance record to the session
                    defaults={'status': status}
                )

        # Pass the course and the flag to the context
        # as this post request is going to render the confirmation page
        context["class"] = course.course_name
        context["is_professor"] = True

        # Redirect to the confirmation page
        return render(request, "home/confirmation.html", context)
    

# ConfirmationView: view that renders the confirmation page
# for student
class ConfirmationView(LoginRequiredMixin, View):
    
    # Template to render
    template_name = "home/confirmation.html"
    
    # Method triggered when a GET request hits the url
    def get(self, request):
        context = {}
        
        # Get the class_id from the session and query the course
        class_id = request.session.get('selected_class_id')
        course = get_object_or_404(Course, id=class_id)
        
        # Assign the course to the context
        # a flag is passed to the template to
        # indicate that the user is not a professor
        context["class"] = course.course_name
        context["is_professor"] = False
        
        return render(request, self.template_name, context)
    
# StudentAttendanceView: view that renders the student attendance page
class StudentAttendanceView(LoginRequiredMixin, View):
    
    # Template to render
    template_name = 'home/student_attendance.html'

    # Method triggered when a GET request hits the url
    def get(self, request):
        
        context = {}
        
        # Query the student and his courses
        student = get_object_or_404(Student, user=request.user)
        context['courses'] = student.courses.all()
        
        # Render the template with the given context
        return render(request, self.template_name, context)

    # Method triggered when a POST request hits the url
    def post(self, request):
        context = {}
        
        # Get the selected course from the POST request
        selected_course_id = request.POST.get('selected_course')
        
        # Query the course and the student from the selected course
        course = get_object_or_404(Course, id=selected_course_id)
        student = get_object_or_404(Student, user=request.user)
        
        # Query the attendance records related to the student and course
        attendance_records = Attendance.objects.filter(student=student, session__course=course)
        
        # Assign the course, student and attendance records to the context
        context['courses'] = student.courses.all()
        context['selected_course'] = course
        context['student'] = student
        context['attendance_records'] = attendance_records

        # Render the template with the given context
        return render(request, self.template_name,context)
    
# ProfessorAttendanceView: view that renders the professor attendance page
class ProfessorAttendanceView(LoginRequiredMixin, View):
    
    # Template to render
    template_name = 'home/professor_attendance.html'

    # Method triggered when a GET request hits the url
    def get(self, request):
        
        context = {}
        
        # Query the professor and his courses
        professor = get_object_or_404(Professor, user=request.user)
        sessions = Session.objects.filter(course__in=professor.courses.all())
        
        # Assign the courses and session for the professor to the context
        context['courses'] = professor.courses.all()
        context['sessions'] = sessions
        
        # Render the template with the given context
        return render(request, self.template_name, context)

    # Method triggered when a POST request hits the url
    def post(self, request):
        context = {}
        
        # Get the selected course and session from the POST request
        selected_course_id = request.POST.get('selected_course')
        selected_session_number = request.POST.get('selected_session')
        
        # Query the course, session and professor from the selected course
        course = get_object_or_404(Course, id=selected_course_id)
        session = get_object_or_404(Session, course=course, session_number=selected_session_number)
        professor = get_object_or_404(Professor, user=request.user)
        
        # Query all the sessions related a given course
        sessions = Session.objects.filter(course__in=professor.courses.all())
        
        # Assign the attendance records, course, session and courses for the professor to the context
        context['attendance_records'] = Attendance.objects.filter(session=session)
        context['selected_course'] = course
        context['selected_session'] = session
        context['sessions'] = sessions
        context['courses'] = professor.courses.all()

        # Render the template with the given context
        return render(request, self.template_name, context)
    
# The following views are used to call the Azure Functions
# from the frontend. This is done to avoid exposing the
# API keys on the client side.

# call_azure_function: view that calls the Azure Function that
# generates the attendance codes
def call_azure_function(request):
    
    # Send a GET request to the Azure Function
    response = requests.get(
        settings.GENERATE_CODE_FUNC ,
        params={'code': settings.GENERATE_CODE_KEY}
    )
    # If the response is 200, return the JSON response
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
    # Else return an error
        return JsonResponse({'error': 'Failed to fetch data from Azure Function'}, status=500)

# call_delete_function: view that calls the Azure Function that
# deletes the attendance codes in the Azure Table
def call_delete_function(request):
    
    # Send a GET request to the Azure Function
    response = requests.get(
        settings.DELETE_CODE_FUNC ,
        params={'code': settings.DELETE_CODE_KEY}
    )
    # If the response is 200, return the JSON response (successful deletion)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
    # Else return an error
        return JsonResponse({'error': 'Failed to fetch data from Azure Function'}, status=500)