from urllib import request

from django import forms
from django.shortcuts import get_object_or_404

from .models import Post, Category, User


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Category',
    )

    # author = forms.ModelChoiceField(
    #     queryset=User.objects.filter(),
    #     label='Автор',
    # )

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
            'category',
            'type'
        ]

