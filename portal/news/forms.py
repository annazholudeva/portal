from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Category',
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
            'category',
            'type'
        ]
    # class Meta:
    #     model = Post
    #     fields = ['author',
    #               'title',
    #               'content',
    #               # 'type',
    #               'category']
