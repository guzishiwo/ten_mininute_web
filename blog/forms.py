from django import forms
from django.forms import ModelForm
from blog.models import Comment


class CommentForm(ModelForm):
    # belong_to = forms.CharField(required=False, widget=forms.HiddenInput())

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

