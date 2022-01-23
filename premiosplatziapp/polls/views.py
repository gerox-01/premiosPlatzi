from django.shortcuts import render
#Respuesta HTTP
from django.http import HttpResponse
from .models import Question, Choice

# Create your views here.
def index(request):
    # latest_question_list = Question.objects.filter('-pub_date')[:5]
    latest_question_list = Question.objects.all()
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)