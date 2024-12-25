from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.contrib import auth

from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    next_page = forms.CharField(widget=forms.HiddenInput())


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }
    
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        data = super().clean()
        if data["password"] != data["password_confirmation"]:
            raise ValidationError("Passwords do not match")
        return data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user
    
    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = auth.authenticate(request, username=username, password=password)
        auth.login(request, user)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        exclude = ["user", "rating"]
    

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ["password"]


class PasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password"]
        exclude = ["username", "email"]
        widgets = {
            "password": forms.PasswordInput()
        }
    
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        data = super().clean()
        if data["password"] != data["password_confirmation"]:
            raise ValidationError("Passwords do not match")
        return data


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "text", "tags"]
        wigets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]

    question_id = forms.CharField(widget=forms.HiddenInput())
    