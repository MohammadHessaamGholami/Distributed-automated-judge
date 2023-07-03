from django.urls import path
from .views import do_judge


app_name = 'judge'
urlpatterns = [
    path('', do_judge, name='judge')
]