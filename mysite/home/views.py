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
                        date=date,
                        defaults={'status': 'present'}
                    )
                    session.attendance_records.add(attendance_record)

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

        today = timezone.now().date()
        new_session = Session.objects.create_new_session(course=selected_class, date=today)

        context["selected_class"] = selected_class
        context["students"] = students
        context["current_session"] = new_session

        return render(request, self.template_name, context)

    def post(self, request):
        return redirect('display_codes')

class GetAttendance(View):
    def get(self, request):
        data = {}

        class_id = request.GET.get('class_id')
        session_number = request.GET.get('session_number')  # Retrieve session number from request
        selected_class = get_object_or_404(Course, id=class_id)

        try:
            # Fetch the session using both course and session number
            session = Session.objects.get(course=selected_class, session_number=session_number)
        except Session.DoesNotExist:
            session = None

        students_data = []
        for student in Student.objects.filter(courses=selected_class):
            if session:
                attendance_record = session.attendance_records.filter(student=student).first()
                status = attendance_record.status if attendance_record else 'absent'
            else:
                status = 'absent'  # Default to 'absent' if no session is found
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'status': status,
            })

        data['students'] = students_data
    
        return JsonResponse(data)
        
class SubmitAttendanceView(LoginRequiredMixin, View):
    def post(self, request):
        class_id = request.session.get('selected_class_id')
        session_number = request.POST.get('session_number')  # Get session number from POST data
        selected_class = get_object_or_404(Course, id=class_id)

        session, created = Session.objects.get_or_create(
            course=selected_class,
            session_number=session_number
        )

        for student in Student.objects.filter(courses=selected_class):
            status = request.POST.get(f'status_{student.id}')
            attendance_record, created = Attendance.objects.update_or_create(
                student=student,
                date=session.date,  # Ensure attendance record is linked to the session's date
                defaults={'status': status}
            )
            session.attendance_records.add(attendance_record)

        return redirect('home')
    
class ConfirmationView(LoginRequiredMixin, View):
    template_name = "home/confirmation.html"
    def get(self, request):
        context = {}
        class_id = request.session.get('selected_class_id')
        context["class"] = class_id
        return render(request, self.template_name)