from django.db import models
from django.core import validators

# Create your models here.

class Racing(models.Model):
    name = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    presenter = models.ForeignKey("accounts.Teacher", on_delete=models.CASCADE)

    class Meta:
        db_table = "Racing"
    def __str__(self):
        return self.name

        
class Question(models.Model):
    title = models.CharField(max_length=50)
    question = models.FileField(upload_to='Question/question', blank=False, null=False)
    sample_input = models.FileField(upload_to='Question/sample_input', blank=False, null=False)
    sample_output = models.FileField(upload_to='Question/sample_output', blank=False, null=False)
    #answer = models.FileField(upload_to='Question/answer', blank=True, null=True)
    #is_sent =models.BooleanField(default=False)
    #is_accepted = models.BooleanField(default=False)
    racing = models.ForeignKey(Racing, on_delete=models.CASCADE)
    #student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        db_table = "Question"
        #unique_together = ("racing", "student", "question")
    def __str__(self):
        return self.title
class StudentRacing(models.Model):
    racing = models.ForeignKey(Racing, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)

    class Meta:
        db_table = "StudentRacing"
        unique_together = ("racing","student")

class StudentQuestion(models.Model):
    answer = models.FileField(upload_to='StudentQuestion/answer', blank=False, null=False)
    is_accept = models.BooleanField(default=False)
    
    answer_score = models.IntegerField(default=0)
    sending_at = models.DateTimeField(auto_now_add=True)
    running_time = models.CharField(max_length=30, default="0")
    
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, blank=True, null=True)
    racing = models.ForeignKey(Racing, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    class Meta:
        db_table = "StudentQuestion"
        unique_together = ("student", "racing", "question")
        