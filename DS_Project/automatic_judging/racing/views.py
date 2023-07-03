from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from racing.models import Racing, StudentRacing, Question, StudentQuestion
from .forms import RacingForm, QuestionForm, StudentQuestionForm
from django.db import models 
from racing.LoadBalancer import add_queue
import os
import requests
import json


# Create your views here.


@login_required
def racing_list(request):
    
    cs = Racing.objects.raw("""select r.id, presenter_id, name, count(jr.student_id) as member_count from "Racing" as r left outer join "StudentRacing" as jr on r.id = jr.racing_id group by r.id """)
    cs = list(filter(lambda x: StudentRacing.objects.filter(student_id=request.user.id, racing_id=x.id).exists() or
                               x.presenter_id == request.user.role.pk, cs))
    form = RacingForm(request.POST or None)

    # list of racing that the user is not in.
    a1 = list(Racing.objects.raw("""select r.id, name, time from "Racing" as r EXCEPT select r.id, name, time from "Racing" as r left outer join "StudentRacing" as jr on r.id = jr.racing_id where jr.student_id = %s """, [request.user.role.pk]))
    
    # list of racing that the user is in.
    a2 = list(Racing.objects.raw("""select r.id, name, time from "Racing" as r left outer join "StudentRacing" as jr on r.id = jr.racing_id where jr.student_id = %s """, [request.user.role.pk]))

    if request.method == 'POST' and request.user.TYPE_TEACHER:
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""insert into "Racing" (name, time, is_active, presenter_id) values (%s, %s, %s, %s) """,
                [form.cleaned_data['name'], form.cleaned_data['time'],False 
                ,request.user.role.pk])
                messages.add_message(request, messages.SUCCESS, "مسابقه ایجاد شد.")
            return redirect('racing:racing_list')
    return render(request, 'racing/index.html', {'is_teacher':request.user.type == request.user.TYPE_TEACHER, 'form': form, 'racing_list': cs, 'membered_racing':a2, 'not_membered_racing':a1})

@login_required
def join_racing(request, racing_id):
    with connection.cursor() as cursor:
        cursor.execute("""insert into "StudentRacing" (racing_id, student_id) values (%s, %s) """,[racing_id, request.user.role.pk])
    return redirect('racing:racing_list')

@login_required
def racing_questions(request, racing_id):
    get_object_or_404(Racing, id=racing_id)
    questions = Question.objects.raw("""select * from "Question" as q where q.racing_id = %s """,[racing_id])
    question_form = QuestionForm()
    racing_name = Racing.objects.raw("""select * from "Racing" as r where r.id = %s  """,[racing_id])
    if request.method == "POST":
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
                question = question_form.save(commit=False)
                question.racing_id = racing_id
                question.save()
                messages.add_message(request, messages.SUCCESS, "سوال ایجاد شد.")
                return redirect('racing:racing_questions', racing_id=racing_id)
    return render(request, 'racing/racing_questions.html', {'questions':questions, 'racing_id': racing_id, 'question_form': question_form, 'is_teacher': request.user.type == request.user.TYPE_TEACHER,'racing_name': racing_name})


@login_required
def add_answer(request, racing_id, question_id):
    #print("*/*/*/*/")
    if request.method == "POST":
        answer_form = StudentQuestionForm(request.POST, request.FILES)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            
            ########################################## add answer_code to queue!
            answer.racing_id = racing_id
            answer.question_id = question_id
            answer.student_id = request.user.role.pk
            answer.is_accept = False
            answer.answer_score = -1
            answer.running_time = ' '
            answer.save()
            
            code=StudentQuestion.objects.get(racing_id=racing_id, question_id=question_id, student_id=request.user.role.pk).answer.path
            code = answer.answer.path
            sample_input = Question.objects.get(id = question_id).sample_input.path
            sample_output = Question.objects.get(id = question_id).sample_output.path
            #checkCode = "/home/hesam/Desktop/DistributedSystems/DS_Project/automatic_judging/racing/check.py"
            checkCode = "config/check.py"

            #print(sample_input)
            #print(sample_output)
            #print(code)
            #print(checkCode)
            add_queue(code, sample_input, sample_output, checkCode, request.user.role.pk, question_id, racing_id)
            #distribute_work(code, sample_input, sample_output, checkCode)
            

            messages.add_message(request, messages.SUCCESS, "جواب با موفقیت تحویل داده شد.")
    return redirect('racing:question_detail', racing_id=racing_id, question_id=question_id)



@login_required
def question_detail(request, racing_id, question_id):
    question = Question.objects.raw("""select * from "Question" as q where q.racing_id = %s and q.id = %s""",[racing_id, question_id])
    is_sentAnswer = bool(StudentQuestion.objects.filter(question_id=question_id, racing_id=racing_id, student_id=request.user.role.pk).count())
    #print(is_sentAnswer)
    answer_form = StudentQuestionForm(request.POST, request.FILES)
    the_answer = []
    answers_of_question = []
    if (is_sentAnswer):
        the_answer = StudentQuestion.objects.raw("""select * from "StudentQuestion" where racing_id=%s and question_id=%s and student_id=%s """,
        [racing_id, question_id, request.user.role.pk]
        )
    answers_of_question = StudentQuestion.objects.raw(""" select * from "StudentQuestion" as sq join "Student" as s on sq.student_id=s.student_id where question_id=%s and racing_id=%s order by answer_score """,
    [question_id, racing_id ])
    return render(request, 'racing/question_detail.html', {'question': question, 'racing_id': racing_id,'question_id':question_id, 'is_sentAnswer': is_sentAnswer, 'the_answer': the_answer, 'answer_form':answer_form, 'is_teacher': request.user.type == request.user.TYPE_TEACHER,'answers_of_question': answers_of_question})
    
@login_required
def delete_answer(request, racing_id, question_id):
    
    if request.method == "GET":
        StudentQuestion.objects.filter(question_id=question_id, racing_id=racing_id, student_id=request.user.role.pk).delete()
        #with connection.cursor() as cursor:
        #    cursor.execute("""delete from "StudentQuestion" where racing_id=%s and question_id=%s and student_id=%s """,
        #[racing_id, question_id, request.user.role.pk]
        #)
        messages.add_message(request, messages.SUCCESS, "جواب با موفقیت حذف شد.")

    return redirect('racing:question_detail', racing_id=racing_id, question_id=question_id)
