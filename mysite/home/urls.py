from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ConfirmationView, AttendanceManagementeView, DisplayCodesView, ProfessorDashboardView, StudentAttendanceView, ProfessorAttendanceView

# URL patterns for the app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomeView.as_view(), name = "home"),
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('professor/', ProfessorDashboardView.as_view(), name='professor_dashboard'),
    path('professor/display_codes/', DisplayCodesView.as_view(), name ='display_codes'),
    path('student/confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('professor/display_codes/validate/', AttendanceManagementeView.as_view(), name="attendance_management"),
    path('student/attendance/', StudentAttendanceView.as_view(), name='student_attendance'),
    path('professor/attendance/', ProfessorAttendanceView.as_view(), name='professor_attendance'),
]