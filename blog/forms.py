from django import forms

#forms 안에있는 모델폼을 가지고 커멘트 폼을 만들것이다.
from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
