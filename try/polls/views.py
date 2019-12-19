from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_list_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

def questionnaire(request):
    data = Question.objects.all()

    return render(request, 'polls/questionnaire.html', {'data': data})

class DetailView(generic.DetailView):
    model=Question
    data = Question.objects.all()
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request):
    questions = get_list_or_404(Question)
    try:
        for question in questions:
            # Get the list of ids from the list of radio buttons
            selected_choices_pk = request.GET.getlist(question.question_text)
            selected_choices = Choice.objects.filter(pk__in=selected_choices_pk)
            selected_choices.update(votes=F('votes') + 1)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
    finally:
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


