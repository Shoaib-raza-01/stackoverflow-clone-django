from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistrationForm, QuestionForm
from django.db.models import Count
from . import models


# Create your views here.

def register(request):
    # if(request.user.username):
    #     return redirect('authenticate:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('authenticate:home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {"form" : form})

def home_page(request):
    user=request.user
    questions = models.Question.objects.annotate(answer_count=Count('answer')).order_by('-CreatedAt')[:20]
    
    for question in questions:
        question.tag_list = [tag.strip() for tag in question.Tags.split(',')]
        
    context = {
        "questions": questions,
        "user" : user,
        # "tags" : tags
    }
    return render(request, "homepage.html", context)


def login_view(request):
    # if(request.user.username):
    #     return redirect("authenticate:home")
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
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



def ask_question_view(request):
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

def question_detail(request, question_id):
    question = get_object_or_404(models.Question, id=question_id)
    
    question.tag_list = question.Tags.split(",")
    
    if request.method == 'POST':
        input_type = request.POST.get("input_type")
        if input_type == "up":
            question.votes +=1
        if input_type == "down":
            question.votes -= 1
        question.save()
        return redirect('authenticate:question-detail', question_id=question.id)
    return render(request, 'question-detail.html', {'question': question})























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