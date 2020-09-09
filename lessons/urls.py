from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'lessons'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('<int:lesson_id>/comment/', views.comment, name='comment'),
    path('articles', views.AllArticleView.as_view(), name='all_articles')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
