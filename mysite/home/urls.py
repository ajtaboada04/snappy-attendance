from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ProfessorDashboardView
from .views import DisplayCodesView

urlpatterns = [
    path('', views.HomeView.as_view(), name = "home"),
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('submit/attendance/', views.StudentDashboardView.as_view(), name='submit_attendance_code'),
    path('professor/', ProfessorDashboardView.as_view(), name='professor_dashboard'),
    path('professor/display_codes/', DisplayCodesView.as_view(), name ='display_codes')
]
