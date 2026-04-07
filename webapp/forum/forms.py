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
                'placeholder': 'Dodaj tytuł...'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Dodaj opis...'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, *args, **kwargs):
        post_type = kwargs.pop("post_type", None)
        super().__init__(*args, **kwargs)

        # jeśli przepis to dodaj pola
        if post_type == "RECIPE":
            self.show_recipe_fields = True

            self.fields['ingredients'] = forms.CharField(
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Składniki'
                }),
                required=True
            )

            self.fields['calories'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Kalorie'
                })
            )

            self.fields['servings'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Liczba porcji'
                })
            )

            self.fields['time'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Czas przygotowania'
                })
            )


#dodawanie komentarzy
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']