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

def question_detail(request, question_id):
    question = get_object_or_404(models.Question, id=question_id)
    answers = models.Answer.objects.filter(question=question)
    comment_form = forms.CommentForm(request.POST)
    answer_form = forms.AnswerForm(request.POST)
    question.tag_list = question.Tags.split(" ")
    bookmark= None
    if request.user.is_authenticated:
        bookmark = models.BookMarked.objects.filter(user=request.user, question=question).first()
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
                return redirect(request.META.get('HTTP_REFERER'))

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
            
        elif input_type == "ques-bookmark":
            bookmarked = models.BookMarked.objects.filter(user=request.user, question=question).exists()
            
            if not bookmarked:
                models.BookMarked.objects.create(user=request.user, question=question, isBookMarked=True)
                # bookmark = models.BookMarked.objects.filter(user=request.user, question=question).first()
                print("created the bookmark")
                return redirect('authenticate:question-detail', question_id=question.id)
            else:
                models.BookMarked.objects.filter(user=request.user, question=question).delete()
                print("deleted the bookmark created")
                
                return redirect('authenticate:question-detail', question_id=question.id)
    else:
        print("login required")
        # bookmark=""
    context = {
        'question': question, 
        'answers': answers, 
        'form': comment_form, 
        'answer_form': answer_form,
        'bookmark': bookmark
        }

    return render(request, 'question-detail.html', context)

def saved_view(request):
    if request.user.is_authenticated:
        user_info = models.UserInformation.objects.get(user=request.user)
        bookmarked = models.BookMarked.objects.filter(user=request.user)
        tag_list=[]
        for i in bookmarked:
            print(i.question.Tags)
            
            tag_list.append(i.question.Tags)
        print(tag_list)
        context = {
            "user_info": user_info,
            "bookmarked": bookmarked,
            'tag_list': tag_list,
            'view_template': 'all-saved.html'
        }
        return render(request, 'saved.html', context)
    return redirect("authenticate:login")

def profile_view(request):
    return HttpResponse("profilepage")

def edit_view(request):
    user_info = models.UserInformation.objects.get(user=request.user)

    if request.method == "POST":
        edit_form = forms.UserInfoForm(request.POST, request.FILES, instance=request.user.userinformation)
        if edit_form.is_valid():
            # edit = edit_form.save(commit=False)
            # edit.user = request.user
            edit_form.save()
            
            # cleaned_data = edit_form.cleaned_data
            
            
            # name = edit_form.cleaned_data.get("Name")
            # print(name)
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        edit_form = forms.UserInfoForm(instance=request.user.userinformation)

    context ={
        "user_info": user_info,
        'view_template': 'edit-profile.html',
        'edit_form': edit_form
    }
    return render(request, 'saved.html', context)

def logout_view(request):
    if request.user:
        logout(request)
    return redirect("authenticate:home")