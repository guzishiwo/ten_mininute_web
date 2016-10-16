from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm
from website.models.user import UserProfile
from website.models.articles import Comment


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


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password1")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password']:
            self.fields[field_name].help_text = None


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


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Enter Your old password (Required)"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Enter Your new password (Required)"}
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Enter Your confirms password (Required)"}
    ))

    def clean_confirm_password(self):
        old_password = self.cleaned_data.get("old_password")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password and password == old_password:
            raise forms.ValidationError("Passwords do not match!!!")
        return confirm_password


class ChangeUserInfoForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('belong_to', 'last_activity')

    # def __init__(self, *args, **kwargs):
    #     super(ChangeUserInfoForm, self).__init__(*args, **kwargs)
