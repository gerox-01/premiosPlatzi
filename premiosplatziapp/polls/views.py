from django.shortcuts import render, get_object_or_404
#Respuesta HTTP
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
# def index(request):
#     # latest_question_list = Question.objects.filter('-pub_date')[:5]
#     latest_question_list = Question.objects.all()
#     return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {
#         'question': question
#     })


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class indexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #El menos significa que ordena de las mas recientes a las mas antiguas
        #Antiguo código
        # return Question.objects.filter('-pub_date')[:5]
        #Nuevo código - let: less then equal to timezone.now()
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
class detailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class resultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    #Le enviamos un question_id a la vista vote.html
    question = get_object_or_404(Question, pk=question_id)
    try:
        #El método es post, dónde se accede a los datos del formulario - si existe hace esto sino va al except
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
        {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else: 
        #Por cada voto se incrementa en uno la BD
        selected_choice.votes += 1
        #Guardamos los cambios en la BD
        selected_choice.save()
        #Redireccionamos a la vista results
        #Args es una tupla, por eso se pone la coma
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))