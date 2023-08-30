from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date')  #
    list_filter = ('category__category_name', 'date')
    search_fields = ('title', 'category__category_name')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
