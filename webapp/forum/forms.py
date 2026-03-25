from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'post_type']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your post...'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            })
        }

#dodawanie komentarzy
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']