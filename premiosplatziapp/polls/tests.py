import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

#TestCase es un conjunto de test que nos permite ejecutar varios
#Vas a testear modelos o vistas. Es lo más común.
class QuestionModelTest(TestCase):
    
    #Crear un nombre que sea descriptivo
    def test_was_published_recently_with_future_questions(self):
        """   was_published_recently return False for questions whose pub_date is in the future   """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quién es el mejor Course Director  de Platzi?", pub_date=time)
        #Verfificar que el resultado de la función es False. Es un assertIs que afirma que el resultado de la función es False
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """   was_published_recently return True for questions whose pub_date is in the present   """
        time = timezone.now() - datetime.timedelta(days=1)
        present_question = Question(question_text="¿Quién es el mejor Course Director  de Platzi?", pub_date=time)
        #Verfificar que el resultado de la función es True. Es un assertIs que afirma que el resultado de la función es True
        self.assertIs(present_question.was_published_recently(), True)
    
    def test_was_published_recently_with_old_questions(self):
        """   was_published_recently return False for questions whose pub_date is older than 1 day   """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(question_text="¿Quién es el mejor Course Director  de Platzi?", pub_date=time)
        #Verfificar que el resultado de la función es False. Es un assertIs que afirma que el resultado de la función es False
        self.assertIs(old_question.was_published_recently(), False)


def create_question(question_text, days):
    """
    Create a question with the given "question_text", and published the given number
    of days offset to now (negative for question published in the past positive for question that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_question_futures(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page.
        """
        create_question(question_text="¿Quién es el mejor Course Director  de Platzi?", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_public_date_old(self):
        """"
        Questions with a pub_date in the past are displayed in the index page.
        """
        question = create_question(question_text="¿Quién es el mejor Course Director  de Platzi?", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question are displayed
        """
        past_question = create_question(question_text="Past Question", days=-30)
        future_question = create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        past_question_1 = create_question(question_text="Past Question 1", days=-30)
        past_question_2 = create_question(question_text="¿Past Question 2", days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_1, past_question_2])

    def test_two_future_question(self):
        """
        The questions index page may display multiple questions.
        """
        future_question_1 = create_question(question_text="Future Question 1", days=30)
        future_question_2 = create_question(question_text="Future Question 2", days=40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 error not found
        """
        future_question = create_question(question_text="Future Question", days=30)
        #Los args son una tupla
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
