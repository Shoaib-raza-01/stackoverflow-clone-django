from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    what_you_try = models.TextField()
    Tags = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        # return super().__str__()
        return self.Title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Content = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    Likes = models.IntegerField(default=0)
    flag = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["-CreatedAt"]

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Content = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    
    
class QuestionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4)

    class Meta:
        unique_together = ('user', 'question')
        
class AnswerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4)

    class Meta:
        unique_together = ('user', 'answer')
        
class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30, blank=True)
    Title = models.CharField(max_length=20, blank=True)
    Profile_image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    Location = models.CharField(max_length=70, blank=True)
    About = models.TextField(blank=True)
    CreatedAt = models.DateField(auto_now_add=True)
    Website_link = models.CharField(max_length=70, blank=True)
    Github_link = models.CharField(max_length=70, blank=True)
    Twitter_link = models.CharField(max_length=70, blank=True)
    
class BookMarked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    isBookMarked = models.BooleanField(default=False)
    