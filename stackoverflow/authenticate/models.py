from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
    # class Meta:
    #     verbose_name_plural = 'customuser'

    # def __str__(self):
    #     return self.email


# class User(models.Model):
#     # image = models.URLField()
#     bio = models.TextField()
#     phone = models.CharField(max_length=15, unique=True)
#     UserName = models.CharField(max_length=255, unique=True)
#     Email = models.EmailField(unique=True)
#     Password = models.CharField(max_length=255)

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    what_you_try = models.TextField()
    Tags = models.CharField(max_length=100)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Content = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    Likes = models.IntegerField()

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Content = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    Likes = models.IntegerField()
