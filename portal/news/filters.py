from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория')

    title = ModelChoiceFilter(
        field_name='title',
        queryset=Post.objects.all(),
        label='Название')

    date = DateFilter(
        field_name='date',
        label='Дата (позже)',
        lookup_expr='lt',
        widget=DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )

    class Meta:
        model = Post
        fields = {
            'category',
            'title',
            'date'
    }