from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .QusetionForm import QuestionForm
from .models import Question
import json
import os

# Create your views here.

@csrf_exempt 
def do_judge(request):
    print("*****receive request for judging*****")
    data = {}
    if request.method == "POST":
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=True)
            item = Question.objects.get(id=question.id)
            #print(item.code.path)
            #print(item.sample_input.path)
            #print(item.sample_output.path)
            #print(item.checkCode.path)

            result = os.popen("python3 "+item.checkCode.path+' '+item.code.path+ ' '+ item.sample_input.path + ' ' + item.sample_output.path).readline()
            result = result.split(' ')
            #print(result)
            data['running_time'] = result[0]
            data['score'] = result[1]
            data = json.dumps(data)

        return HttpResponse(data, content_type='application/json')
