from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')

# class EmailAuthenticationForm(AuthenticationForm):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

#     def clean_username(self):
#         return self.cleaned_data['email']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = [
            'Title',
            'Description',
            'what_you_try',
            'Tags'
        ]