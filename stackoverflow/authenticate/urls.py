from django.urls import path
from . import views

app_name = "authenticate"
urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('ask/', views.ask_question_view, name='ask-question'),
    path('question/<int:question_id>/', views.question_detail, name='question-detail'),
]