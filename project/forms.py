from django import forms
from .models import Student

class SignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["username", "last_name", "number", "password"]