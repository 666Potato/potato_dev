from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.utils.decorators import method_decorator

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

    # Object created
    new_comment = Comment.objects.create(topic=lesson, comment_text=request.POST['comment_text'],
                                         posted_by=request.user)

    # Create queryset and transform into json
    user = request.user.get_username()
    return JsonResponse({"comment_text": new_comment.comment_text, "posted_by": user})
