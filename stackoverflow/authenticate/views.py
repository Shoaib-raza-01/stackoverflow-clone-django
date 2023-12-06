from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistrationForm, QuestionForm
from django.db.models import Count, Q
from . import models
from . import forms


# Create your views here.

def register(request):
    if(request.user.is_authenticated):
        return redirect('authenticate:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            # modelname.objects.create(user = req.user)
            return redirect('authenticate:home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {"form" : form})

def home_page(request):
    user=request.user
    questions = models.Question.objects.annotate(answer_count=Count('answer')).order_by('-CreatedAt')[:20]
    
    if request.method == 'POST':
        input_value = request.POST.get("input-value")
        question_array = models.Question.objects.filter(
    Q(Title__icontains=input_value) | Q(Tags__icontains=input_value)
)

        questions =  question_array
        
    
    for question in questions:
        question.tag_list = [tag.strip() for tag in question.Tags.split(',')]
        
    context = {
        "questions": questions,
        "user" : user,
        # "tags" : tags
    }
    return render(request, "homepage.html", context)


def login_view(request):
    if(request.user.is_authenticated):
        return redirect("authenticate:home")
    error=''
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('authenticate:home')
        else:
            error = "Invalid username/password"
    # else:
    form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, "errors":error})



def ask_question_view(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.user = request.user
                question.save()
                return redirect('authenticate:home')
        else:
            form = QuestionForm()
        
        return render(request, 'ask-question.html', {'form': form})
    else:
        return redirect("authenticate:login")
# def question_detail(request, question_id):
#     question = get_object_or_404(models.Question, id=question_id)
#     answers = models.Answer.objects.filter(question=question)
#     comment_form = forms.CommentForm(request.POST)
#     answer_from = forms.AnswerForm(request.POST)
#     question.tag_list = question.Tags.split(",")
    
#     if request.method == 'POST':
#         input_type = request.POST.get("input_type")
#         if input_type in ("up", "down"):
#             if input_type == "up":
#                 question.votes += 1
#             elif input_type == "down":
#                 question.votes -= 1
#             question.save()
            
#         elif input_type in ("answer-up", "answer-down"):
#             answer_id_str = request.POST.get("answer_id")
#             if answer_id_str is not None:
#                 answer_id = int(answer_id_str)
#                 answer = get_object_or_404(models.Answer, id=answer_id)

#                 if input_type == "answer-up":
#                     answer.Likes += 1
#                 elif input_type == "answer-down":
#                     answer.Likes -= 1
#                 answer.save()
#                 return redirect('authenticate:question-detail', question_id=answer.question.id)
            
#         elif input_type == "answer-comment":
#             if comment_form.is_valid():
#                 comment = comment_form.save(commit=False)
#                 comment.user = request.user
#                 comment.answer = get_object_or_404(models.Answer, id=int(request.POST['answer_id']))
#                 comment.save()
#                 return redirect('authenticate:question-detail', question_id=comment.answer.question.id)
            
#         elif comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.user = request.user
#             comment.question = question
#             comment.save()
#             return redirect('authenticate:question-detail', question_id=question.id) 
        
#         elif answer_from.is_valid():
#             answer = answer_from.save(commit=False)
#             answer.user = request.user
#             answer.question = question
#             print("done")
#             answer.save()
#             return redirect('authenticate:question-detail', question_id=question.id) 
            
            
            

        
#     return render(request, 'question-detail.html', {'question': question, 'answers': answers, 'form': comment_form, 'answer_form': answer_from})
def question_detail(request, question_id):
    question = get_object_or_404(models.Question, id=question_id)
    answers = models.Answer.objects.filter(question=question)
    comment_form = forms.CommentForm(request.POST)
    answer_form = forms.AnswerForm(request.POST)
    question.tag_list = question.Tags.split(",")
    
    # question.views += 1
    # question.save()

    if request.method == 'POST' and request.user.is_authenticated:
        input_type = request.POST.get("input_type")
        
        voted_question = models.QuestionVote.objects.filter(user=request.user, question=question).first()
        # print(voted_question)
        
        if input_type in ("up", "down"):
            
            if input_type == "up" and not voted_question:
                print("up")
                question.votes += 1
                models.QuestionVote.objects.create(user=request.user, question=question, vote_type="up")
                
            elif input_type == "down" and not voted_question:
                print("down")
                question.votes -= 1
                models.QuestionVote.objects.create(user=request.user, question=question, vote_type="down")

            elif input_type == "down" and voted_question and voted_question.vote_type == "down":
                print("already voted down")
                
            elif input_type == "up" and voted_question and voted_question.vote_type == "up":
                print("already voted up")

            elif input_type == "up" and voted_question and voted_question.vote_type == "down":
                question.votes += 1
                models.QuestionVote.objects.filter(user=request.user, question=question).update(vote_type="up")

            elif input_type == "down" and voted_question and voted_question.vote_type == "up":
                question.votes -= 1
                models.QuestionVote.objects.filter(user=request.user, question=question).update(vote_type="down")
                
                
            question.save()

            
            return redirect('authenticate:question-detail', question_id=question.id)



        elif input_type in ("answer-up", "answer-down"):
            answer_id_str = request.POST.get("answer_id")
            if answer_id_str is not None:
                answer_id = int(answer_id_str)
                answer = get_object_or_404(models.Answer, id=answer_id)
                
                voted_answer = models.AnswerVote.objects.filter(user=request.user, answer=answer).first()
                
                if input_type == "answer-up" and not voted_answer:
                    print("answer-up")
                    answer.Likes += 1
                    models.AnswerVote.objects.create(user=request.user, answer=answer, vote_type="answer-up")
                
                elif input_type == "answer-down" and not voted_answer:
                    print("answer-down")
                    answer.Likes -= 1
                    models.AnswerVote.objects.create(user=request.user, answer=answer, vote_type="answer-down")

                elif input_type == "answer-down" and voted_answer and voted_answer.vote_type == "answer-down":
                    print("already voted down")
                    
                elif input_type == "answer-up" and voted_answer and voted_answer.vote_type == "answer-up":
                    print("already voted up")

                elif input_type == "answer-up" and voted_answer and voted_answer.vote_type == "answer-down":
                    answer.Likes += 1
                    models.AnswerVote.objects.filter(user=request.user, answer=answer).update(vote_type="answer-up")

                elif input_type == "answer-down" and voted_answer and voted_answer.vote_type == "answer-up":
                    answer.Likes -= 1
                    models.AnswerVote.objects.filter(user=request.user, answer=answer).update(vote_type="answer-down")

                answer.save()
                return redirect('authenticate:question-detail', question_id=question.id)

        elif input_type == "answer-comment":
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.answer = get_object_or_404(models.Answer, id=int(request.POST['answer_id']))
                comment.save()
                return redirect('authenticate:question-detail', question_id=question.id)

        elif comment_form.is_valid() and input_type == "comment":
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
            return redirect('authenticate:question-detail', question_id=question.id)

        elif input_type == "answer":
            if answer_form.is_valid(): 
                answer = answer_form.save(commit=False)
                answer.user = request.user
                answer.question = question
                answer.save()
                return redirect('authenticate:question-detail', question_id=question.id)
    else:
        print("login required")
    context = {
        'question': question, 
        'answers': answers, 
        'form': comment_form, 
        'answer_form': answer_form
        }

    return render(request, 'question-detail.html', context)




def profile_view(request):
    pass

def logout_view(request):
    if request.user:
        logout(request)
    return redirect("authenticate:home")
















# def login_view(request):
#     if request.method == 'POST':
#         form = EmailAuthenticationForm(request, request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('authenticate:home')

#     else:
#         form = EmailAuthenticationForm()

#     return render(request, 'login.html', {'form': form})