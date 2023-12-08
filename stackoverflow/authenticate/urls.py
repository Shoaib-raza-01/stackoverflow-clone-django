from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "authenticate"
urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('ask/', views.ask_question_view, name='ask-question'),
    path('question/<int:question_id>/', views.question_detail, name='question-detail'),
    path('saved/', views.saved_view, name='saved-view'),
    
    path('edit/', views.edit_view, name='edit-profile'),
    path('profile/', views.profile_view, name='profile-view'),
    
    path('logout/', views.logout_view, name="logout")
]