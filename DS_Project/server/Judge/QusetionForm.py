from django import forms
from Judge.models import Question



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('code', 'sample_input', 'sample_output', 'checkCode')   
        #fields = ('code',)