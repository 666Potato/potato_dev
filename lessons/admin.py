from django.contrib import admin
from .models import Lesson, Comment, AdditionalMaterialLesson, Articles
# Register your models here.


class MaterialInline(admin.StackedInline):
    model = AdditionalMaterialLesson
    extra = 5


class LessonAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment)
admin.site.register(Articles)

