from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class User(AbstractUser):
    TYPE_STUDENT = 1
    TYPE_TEACHER = 2
    TYPE_CHOICES = (
        (TYPE_STUDENT, 'Student'),
        (TYPE_TEACHER, 'Teacher')
    )
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.email
    
    @property
    def role(self):
        return self.student if self.type == self.TYPE_STUDENT else self.teacher

    def get_full_name(self):
        return self.first_name + " " + self.last_name

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True, verbose_name=_('Student id'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Student"

    def __str__(self):
        return self.student_id

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True, verbose_name=_('Teacher id'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Teacher"

    def __str__(self):
        return self.teacher_id