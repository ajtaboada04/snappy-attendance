from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from .models import Student, Professor, Course, Session, Attendance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import requests
from django.contrib import messages
from django.db.models import Max

# Create your views here.
# This is a little complex because we need to detect when we are
# running in various configurations


class HomeView(View):
    
    template_name = "home/main.html"
    
    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            
            try:
                student = Student.objects.get(user=request.user)
                classes = student.courses.all()
                context['classes'] = classes

            except Student.DoesNotExist:
                context['error'] = "Student profile not found."
                
        return render(request, self.template_name, context)

class StudentDashboardView(LoginRequiredMixin, View):
    template_name = 'home/student_dashboard.html'
    
    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            student = get_object_or_404(Student, user = request.user)
            classes = student.courses.all()
            context['classes'] = classes
            context['student'] = student
        return render(request, self.template_name, context)

    def post(self, request):
        student = get_object_or_404(Student, user=request.user)
        selected_class_id = request.POST.get('selected_class')
        attendance_code = request.POST.get('attendance_code')

        # Get the course using the selected_class_id
        course = get_object_or_404(Course, id=selected_class_id)

        # URL of your Azure Function
        azure_function_url = 'https://tempcodes.azurewebsites.net/api/ValidateCodeFunction?code=4EcQ_77UF2j1CKwIzbYWR1TNhO8KutT81eQahrrJLQvUAzFuIX0j8A=='
        
        try:
            payload = {'code': attendance_code}
            response = requests.post(azure_function_url, json=payload)

            if response.status_code == 200 and response.text == 'true':
                date = timezone.now().date()

                # Find the most recent (or current) session number for this course
                latest_session = Session.objects.filter(course=course).aggregate(Max('session_number'))
                session_number = latest_session['session_number__max']

                if session_number is not None:
                    # Get or create the session for the current day with the latest session number
                    session, _ = Session.objects.get_or_create(course=course, session_number=session_number)

                    # Create or update the attendance record
                    attendance_record, created = Attendance.objects.update_or_create(
                    student=student,
                    session=session,  # Link the attendance record to the session
                    defaults={'status': 'present'}
                )
                    
                    return redirect('confirmation')  # Redirect to a confirmation page
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
        
class ProfessorDashboardView(LoginRequiredMixin, View):
    template_name = 'home/professor_dashboard.html'
    def get(self, request):
        
        # Render the professor dashboard template on GET request
        context = {}
        if request.user.is_authenticated:
            professor = get_object_or_404(Professor, user=request.user)
            classes = professor.courses.all()
            context["classes"] = classes
            context["professor"] = professor
        return render(request, self.template_name, context)

    def post(self, request):
        selected_class_id = request.POST.get('selected_class')
        try:
            request.session['selected_class_id'] = selected_class_id
            today = timezone.now().date()
            selected_class = get_object_or_404(Course, id=selected_class_id)
            new_session = Session.objects.create_new_session(course=selected_class, date=today)
            request.session['session_number'] = new_session.session_number
        except Course.DoesNotExist:
            request.session['error'] = "Class does not exist."
        return redirect('display_codes')

class DisplayCodesView(View):
    template_name = 'home/attendance.html'

    def get(self, request):
        context = {}

        selected_class_id = request.session.get('selected_class_id')
        selected_class = get_object_or_404(Course, id=selected_class_id)
        students = Student.objects.filter(courses=selected_class)
        

        print("Session Number:", request.session['session_number'])

        context["selected_class"] = selected_class
        context["students"] = students
        context["current_session"] = request.session["session_number"]

        return render(request, self.template_name, context)

    def post(self, request):
        return redirect('display_codes')
    
class ConfirmationView(LoginRequiredMixin, View):
    template_name = "home/confirmation.html"
    def get(self, request):
        context = {}
        class_id = request.session.get('selected_class_id')
        course = get_object_or_404(Course, id=class_id)
        context["class"] = course.course_name
        context["is_professor"] = False
        
        return render(request, self.template_name, context)

class AttendanceManagementeView(LoginRequiredMixin, View):
    template_name = "home/attendance_management.html"

    def get(self, request):
        
        class_id = request.session.get('selected_class_id')
        session_number = request.session.get('session_number') 
        
        print(session_number)
        
        context = {}

        selected_class = get_object_or_404(Course, id=class_id)
        session = get_object_or_404(Session, course=selected_class, session_number=session_number)

        students_data = []
        for student in Student.objects.filter(courses=selected_class):
            attendance_record = Attendance.objects.filter(student=student, session=session).first()
            status = attendance_record.status if attendance_record else 'absent'
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'status': status,
            })

        context['selected_class'] = selected_class
        context['current_session'] = session
        context['attendance_records'] = students_data
        
        print(context)
        
        return render(request, self.template_name, context)

    def post(self, request):
        
        context = {}
        
        class_id = request.session.get('selected_class_id')
        session_number = request.session.get('session_number')
            
        course = get_object_or_404(Course, id=class_id) 
            
        session = get_object_or_404(Session, course=course, session_number=session_number)

        for student in Student.objects.filter(courses=course):
        # Get the status from the form
            status = request.POST.get(f'status_{student.id}', 'absent')

            # Update or create the attendance record
            Attendance.objects.update_or_create(
                    student=student,
                    session=session,  # Link the attendance record to the session
                    defaults={'status': status}
                )

        context["class"] = course.course_name
        context["is_professor"] = True

        messages.success(request, "Attendance updated successfully.")
            
        return render(request, "home/confirmation.html", context)