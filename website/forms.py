from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.forms import ModelForm
from website.models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('create_on', 'belong_to')

        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': '填写你的评论'
            }),
        }

        EMPTY_LIST_ERROR = "You can't have an empty"

        error_messages = {
            'content': {'required': EMPTY_LIST_ERROR}
        }

    invalid_words_list = ['admin', 'super_admin', 'super_super_admin']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in self.invalid_words_list:
            if word in name:
                raise forms.ValidationError('Your comment contains invalid words,please check it again.')
        return self.cleaned_data.get('name')


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Incorrect Login Details')

        return self.cleaned_data


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user