from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from .models import Student, Professor, Course, Session, Attendance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
        # Placeholder for handling the form submission
        # Extract the class and code from POST data
        selected_class = request.POST.get('selected_class')
        attendance_code = request.POST.get('attendance_code')
        
        
        
        print(f"Class: {selected_class}, Code: {attendance_code}")

        # You would redirect to a success page or render with a success message
        ctx = {"class":selected_class, "code":attendance_code}

        return render(request, 'home/confirmation.html', ctx)

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
        
        new_session = Session(course=selected_class)
        new_session.save()
        
        context["selected_class"] = selected_class
        context["students"] = students
        

        return render(request, self.template_name, context)
    
    def post(self, request):
        
        return redirect('display_codes')

class GetAttendance(View):
    def get(self, request):
        data = {}
        
        class_id = request.GET.get('class_id')
        selected_class = get_object_or_404(Course, id=class_id)
        students = Student.objects.filter(courses=selected_class)

        students_data = []
        for student in students:
            today = timezone.now().date()
            attendance_record = Attendance.objects.filter(student=student, date=today).first()

            status = attendance_record.status if attendance_record else 'unknown'
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'status': status,
            })

        data['students'] = students_data

        return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class SubmitAttendanceView(View):
    def post(self, request):
        # Process form data
        # Example: request.POST.get('some_field')
        class_id = request.session.get('selected_class_id')
        selected_class = get_object_or_404(Course, id=class_id)

        for student in Student.objects.filter(courses=selected_class):
            status = request.POST.get(f'status_{student.id}')
            date = timezone.now().date()
            Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'status': status}
            )

        # Redirect to main.html after processing
        return redirect('home/main.html')  # Replace 'main' with the name of your URL pattern for main.html

class SubmitCode(View):
    def post(self, request):
        return render(request, "home")