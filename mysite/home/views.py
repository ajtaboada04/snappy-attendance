from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from .models import Student
from django.contrib.auth.mixins import LoginRequiredMixin


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
        print(context)
        return render(request, self.template_name, context)

class StudentDashboardView(LoginRequiredMixin, View):
    template_name = 'home/student_dashboard.html'
    
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

    def post(self, request):
        # Placeholder for handling the form submission
        # Extract the class and code from POST data
        selected_class = request.POST.get('selected_class')
        attendance_code = request.POST.get('attendance_code')

        # Here you would add logic to validate and record the attendance code submission
        # For now, we'll just print it to the console and return a success message
        print(f"Class: {selected_class}, Code: {attendance_code}")

        # You would redirect to a success page or render with a success message
        ctx = {"class":selected_class, "code":attendance_code}

        return render(request, 'home/confirmation.html', ctx)

class ProfessorDashboardView(View):
    def get(self, request):
        # Render the professor dashboard template on GET request
        return render(request, 'home/professor_dashboard.html')

    def post(self, request):
        # Save the selected class to the session
        request.session['selected_class'] = request.POST.get('selected_class')
        # Redirect to the DisplayCodesView
        return redirect('display_codes')  # Assuming 'display_codes' is the name of the URL pattern for DisplayCodesView

class DisplayCodesView(View):
    def get(self, request):
        selected_class = request.session.get('selected_class', 'Default Class')

        static_code = 'ABCD1234'
        context = {
            'selected_class': selected_class,
            'attendance_code': static_code,
        }
        return render(request, 'home/attendance.html', context)
    def post(self, request):
        return redirect('display_codes')
