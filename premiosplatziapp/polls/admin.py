from django.contrib import admin
from .models import Question, Choice

# Register your models here.
class ChoicesInline(admin.StackedInline):
    model = Choice
    can_delete = False
    verbose_name_plural = 'choices'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = (ChoicesInline,)
    #Filtrar
    list_filter = ["pub_date"]
    #Ordenar
    list_display = ["question_text", "pub_date", "was_published_recently"]
    #Buscar
    search_fields = ["question_text"]
    