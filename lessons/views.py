from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Lesson, Comment


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'lessons/index.html'
    context_object_name = 'lessons_list'

    def get_queryset(self):
        # Retrieve all objects
        return Lesson.objects.all()


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
    is_code = request.POST.get('isCode', 0)
    user = request.user.get_username()

    if is_code == 0:
        new_comment = Comment.objects.create(topic=lesson, comment_text=request.POST['comment_text'],
                                             posted_by=request.user)
        return JsonResponse({"comment_text": new_comment.comment_text, "posted_by": user})

    else:
        # Implementation of sandbox. I know it is stupid as eval is executed upon dict, not from file
        with open("my_script.py", "w") as file:
            file.write(request.POST['comment_text'])
        return HttpResponse("handling of sandbox")
