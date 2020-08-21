import time
import subprocess

from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

from lessons.models import Lesson, Comment, Articles


class IndexView(generic.ListView):
    template_name = 'lessons/index.html'
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lessons_list'] = Lesson.objects.all()
        context['articles'] = Articles.objects.all()[:3]
        return context


# @method_decorator(csrf_exempt, name='dispatch')
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = 'lessons/left-sidebar.html'

    def get_queryset(self):
        return Lesson.objects.all()


class ResultView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = 'lessons/no-sidebar.html'


@login_required
@csrf_exempt
def comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    is_code = request.POST.get('isCode')
    user = request.user.get_username()
    timestamp = time.localtime()
    ts = time.strftime("%Y-%m-%d_%H-%M", timestamp)
    filename = "scripts/my_script_{name}_{stamp}.py".format(name=user, stamp=ts)

    if is_code is None:
        new_comment = Comment.objects.create(topic=lesson, comment_text=request.POST['comment_text'],
                                             posted_by=request.user)
        return JsonResponse({"comment_text": new_comment.comment_text, "posted_by": user})

    else:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(request.POST['comment_text'])

        process = subprocess.run("py " + filename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        return HttpResponse(content='<h1>Your output is: </h1>' + process.stdout)
