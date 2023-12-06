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
    path('logout/', views.logout_view, name="logout")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)