from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lesson, Comment


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'lessons/index.html'
    context_object_name = 'lessons_list'

    def get_queryset(self):
        # Retrieve all objects
        return Lesson.objects.all()


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = 'lessons/details.html'

    def get_queryset(self):
        return Lesson.objects.all()


class ResultView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = 'lessons/result.html'


@login_required
def comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)

    # Need to obtain comment_text from form and then assign it to lesson variable
    # declared above. Once it is done, save it with lesson.save()

    Comment.objects.create(topic=lesson, comment_text=request.POST['comment_text'])

    return HttpResponseRedirect(reverse('lessons:result', args=(lesson_id,)))
