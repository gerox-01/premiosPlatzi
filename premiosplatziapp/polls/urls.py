from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.indexView.as_view(), name='index'),
    #ex: /polls/5/
    path('<int:pk>/detail', views.detailView.as_view(), name='detail'),
    #ex: /polls/5/results
    path('<int:pk>/results', views.resultsView.as_view(), name='results'),
    #ex: /polls/5/vote
    path('<int:pk>/vote', views.vote, name='vote'),
]