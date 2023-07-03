from django.urls import path

from .views import student_signup, teacher_signup, authenticate_user, logout_user

app_name = 'accounts'
urlpatterns = [
    path('student-signup/', student_signup, name='student_signup'),
    path('teacher-signup/', teacher_signup, name='teacher_signup'),
    path('login/', authenticate_user, name='login'),
    path('logout/', logout_user, name='logout')
]