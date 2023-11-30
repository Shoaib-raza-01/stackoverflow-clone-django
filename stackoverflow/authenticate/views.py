from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, QuestionForm


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
    return render(request, "homepage.html", {"user" : user})


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