from django.contrib import admin
from .models import Question, Choice

# Register your models here.
class ChoicesInline(admin.StackedInline):
    model = Choice
    can_delete = False
    verbose_name_plural = 'choices'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoicesInline,)