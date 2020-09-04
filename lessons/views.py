from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from lessons.models import Lesson, Comment, Articles


class IndexView(generic.ListView):
    template_name = 'lessons/index.html'
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lessons_list'] = Lesson.objects.all()
        context['articles'] = Articles.objects.all()[:3]
        return context


class DetailView(generic.DetailView):
    model = Lesson
    template_name = 'lessons/left-sidebar.html'

    def get_queryset(self):
        return Lesson.objects.all()


@login_required
@csrf_exempt
def comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    username = request.user.get_username()

    new_comment = Comment.objects.create(topic=lesson, comment_text=request.POST['comment_text'],
                                         posted_by=request.user)
    return JsonResponse({"comment_text": new_comment.comment_text, "posted_by": username})
