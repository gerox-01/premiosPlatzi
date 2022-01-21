from django.shortcuts import render
#Respuesta HTTP
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    # return render(request, 'polls/index.html')
