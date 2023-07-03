from django.db import models

# Create your models here.

class Question(models.Model):
    code = models.FileField(upload_to="Question", blank= False, null=False)
    sample_input = models.FileField(upload_to="Question", blank= False, null=False)
    sample_output = models.FileField(upload_to="Question", blank= False, null=False)
    checkCode = models.FileField(upload_to="Question", blank= False, null=False)
    class Meta:
        db_table = "Question"