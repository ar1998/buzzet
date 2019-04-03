from django import forms
from ocrapp.models import *

class photo_form(forms.ModelForm):
    class Meta:
        model = photo
        fields = ['im',]

class aadhar_from(forms.ModelForm):
    class Meta:
        model = aadhar_registration_model
        fields = ['name','id_num','dob']

class pan_from(forms.ModelForm):
    class Meta:
        model = pan_registration_model
        fields = ['name','id_num','dob']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label = 'Your Password')

    class Meta():
        model = User
        fields = ('username','email','password')