from django import forms
from django.forms.widgets import TextInput, Select, Textarea, FileInput
from racing.models import Question,Racing,StudentRacing, StudentQuestion




class RacingForm(forms.ModelForm):
    class Meta:
        model = Racing
        fields = ('name', 'time')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'maxlength': 50}),
            'time': TextInput(attrs={'class': 'form-control', 'maxlength': 50}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title','question','sample_input','sample_output')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'question': FileInput(attrs={'class': 'form-control-file'}),
            'sample_input': FileInput(attrs={'class': 'form-control-file'}),
            'sample_output': FileInput(attrs={'class': 'form-control-file'}),
        }

class StudentQuestionForm(forms.ModelForm):
    class Meta:
        model = StudentQuestion
        fields = ('answer',)
        widgets = {
            'answer': FileInput(attrs={'class': 'form-control-file'}),
        }