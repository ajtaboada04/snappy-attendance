from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse


# Create your views here.

# This is a little complex because we need to detect when we are
# running in various configurations


class HomeView(View):
    def get(self, request):
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }
        return render(request, 'home/main.html', context)

class StudentDashboardView(View):
    def get(self, request):
        # Render the student dashboard template on GET request
        return render(request, 'home/student_dashboard.html')

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
