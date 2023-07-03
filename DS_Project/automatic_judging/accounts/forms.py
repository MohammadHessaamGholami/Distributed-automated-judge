from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import TextInput

from accounts.models import User, Student, Teacher


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id',)
        widgets = {'student_id': TextInput(attrs={'class': 'form-control', 'maxlength': 10})}


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ('teacher_id',)
        widgets = {
            'teacher_id': TextInput(attrs={'class': 'form-control', 'maxlength': 10}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        label='رمز عبور',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
