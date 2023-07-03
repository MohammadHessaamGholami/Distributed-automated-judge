from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404

from accounts.forms import LoginForm
from accounts.models import User
from .forms import UserCreateForm, StudentForm, TeacherForm

# Create your views here.


def student_signup(request):
    if request.user.is_authenticated:
        return redirect('land_page')
    user_form = UserCreateForm(request.POST or None)
    student_form = StudentForm(request.POST or None)

    if request.method == 'POST':
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.type = User.TYPE_STUDENT
            try:
                user.save()
            except IntegrityError as e:
                print(e)
                raise Http404
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('accounts:login')

    return render(request, 'accounts/student_signup.html', {'user_form': user_form, 'student_form': student_form})





def teacher_signup(request):
    if request.user.is_authenticated:
        return redirect('land_page')
    user_form = UserCreateForm(request.POST or None)
    teacher_form = TeacherForm(request.POST or None)

    if request.method == 'POST':
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.type = User.TYPE_TEACHER
            try:
                user.save()
            except IntegrityError:
                raise Http404
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            return redirect('accounts:login')

    return render(request, 'accounts/teacher_signup.html', {'user_form': user_form, 'teacher_form': teacher_form})


def authenticate_user(request):
    #if request.user.is_authenticated:
     #   return redirect('land_page')

    authentication_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if authentication_form.is_valid():
            user = authenticate(request, email=authentication_form.cleaned_data['email'],
                                password=authentication_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "ورود موفق")
                return redirect('racing:racing_list')
            return redirect('accounts:login')

    return render(request, 'accounts/authenticate.html', {'authentication_form': authentication_form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('land_page')