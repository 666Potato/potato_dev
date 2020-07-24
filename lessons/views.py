from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Lesson, Comment


class IndexView(generic.ListView):
    template_name = 'lessons/index.html'
    context_object_name = 'lessons_list'

    def get_queryset(self):
        # Retrieve all objects
        return Lesson.objects.all()


class DetailView(generic.DetailView):
    model = Lesson
    template_name = 'lessons/details.html'

    def get_queryset(self):
        return Lesson.objects.all()


class ResultView(generic.DetailView):
    model = Lesson
    template_name = 'lessons/result.html'


def comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)

    # Need to obtain comment_text from form and then assign it to lesson variable
    # declared above. Once it is done, save it with lesson.save()
    try:
        """ selected_lesson = request.POST['lesson_id'] """
    except (KeyError, Comment.DoesNotExist):
        return render(request, 'lessons:detail.html', {
            'lesson': lesson,
            'error_message': "You didn't fill comment section",
        })
    else:
        lesson.comment_text = request.POST['comment_text']  # Gives no value
        lesson.save()

        return HttpResponseRedirect(reverse('lessons:result', args=(lesson_id,)))
