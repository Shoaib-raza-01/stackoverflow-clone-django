from django.contrib import admin
from . import models

# Register your models here.

# # admin.site.register(models.User)
# class AnswerInline(admin.StackedInline):
#     model = models.Answer
#     extra = 1

# class CommentInline(admin.StackedInline):
#     model = models.Comment
#     extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('Title', 'user', 'votes')
    # inlines = [AnswerInline]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_question_title', 'Likes', 'user')

    def get_question_title(self, obj):
        return obj.question.Title


class CommentAdmin(admin.ModelAdmin):
    list_display = ('Content', 'question', 'answer', 'user')
    
    
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.UserInformation)
admin.site.register(models.BookMarked)
