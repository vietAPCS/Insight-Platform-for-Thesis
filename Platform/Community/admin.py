from django.contrib import admin
from .models import *
# Register your models here.

class AnswerInline(admin.TabularInline):
    model= Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Community)
admin.site.register(CommunityHistory)
admin.site.register(CommunityDoc)
admin.site.register(CommunityCerti)
admin.site.register(CommunityFormer)
admin.site.register(CommunityQuiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)