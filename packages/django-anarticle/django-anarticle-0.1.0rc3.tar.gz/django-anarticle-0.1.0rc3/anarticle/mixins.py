"""
Copyright (c) 2014-present, aglean Inc.
"""
from django.contrib import admin

from .models import Paragraph


class TagAdminMixin():
    ordering = ('name',)
    list_display = ('id', 'name', 'image', 'image_url', 'article_count')
    search_fields = ('name',)


class CategoryAdminMixin():
    ordering = ('name',)
    list_display = ('id', 'name', 'description', 'image', 'image_url',
                    'tag_count')
    list_filter = ('tags',)
    search_fields = ('name',)
    autocomplete_fields = ('tags',)


class ParagraphInline(admin.StackedInline):
    ordering = ('id',)
    model = Paragraph


class ArticleAdminMixin():
    ordering = ('-created_at',)
    list_display = ('id', 'title', 'author', 'image', 'image_url',
                    'is_published', 'published_at', 'updated_at', 'created_at')
    list_filter = ('tags', 'tags__category')
    search_fields = ('title',)
    inlines = (ParagraphInline,)
    autocomplete_fields = ('tags', 'author')

    def get_changeform_initial_data(self, request):
        return {'author': request.user}
