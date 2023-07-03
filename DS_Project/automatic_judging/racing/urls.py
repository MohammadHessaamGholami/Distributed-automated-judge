from django.urls import path
from .views import racing_list, join_racing, racing_questions, add_answer, question_detail, delete_answer

app_name = 'racing'
urlpatterns = [
    path('', racing_list, name='racing_list'),
    path('<int:racing_id>/', join_racing, name='join_racing'),
    path('<int:racing_id>/questions/', racing_questions, name='racing_questions'),
    path('<int:racing_id>/<int:question_id>/questions/detail', question_detail , name='question_detail'),
    path('<int:racing_id>/<int:question_id>/questions/detail/addAnswer', add_answer , name='add_answer'),
    path('<int:racing_id>/<int:question_id>/questions/detail/deleteAnswer', delete_answer , name='delete_answer')

]