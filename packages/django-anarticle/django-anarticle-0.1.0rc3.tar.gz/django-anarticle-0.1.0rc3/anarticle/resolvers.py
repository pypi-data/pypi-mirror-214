"""
Copyright (c) 2014-present, aglean Inc.
"""
import operator
from functools import reduce

from ariadne import ObjectType, convert_kwargs_to_snake_case
from ariadne_relay import NodeObjectType
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone

from .models import Article, Tag, Category


anarticle_tag = NodeObjectType('AnArticleTag')


@anarticle_tag.instance_resolver
def resolve_anarticle_tag_instance(id, *_):
    return Tag.objects.get(id=id)


@anarticle_tag.connection('articles')
def resolve_anarticle_tag_article_connection(obj, info, **kwargs):
    return resolve_anarticles(obj.article_set.all(), info, kwargs)


@convert_kwargs_to_snake_case
def resolve_anarticle_tags(obj, info, **kwargs):
    name = kwargs.get('name', '')

    queryset = []
    filters = []

    if name:
        filters.append(Q(name__icontains=name))

    if filters:
        queryset = obj.filter(reduce(operator.and_, filters)) \
                if isinstance(obj, QuerySet) \
                else Tag.objects.filter(reduce(operator.and_, filters))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else Tag.objects.all()

    return queryset


anarticle_category = NodeObjectType('AnArticleCategory')


@anarticle_category.instance_resolver
def resolve_anarticle_category_instance(id, *_):
    return Category.objects.get(id=id)


@anarticle_category.connection('tags')
def resolve_anarticle_category_tags(obj, info, **kwargs):
    return resolve_anarticle_tags(obj.tags.all(), info, kwargs)


@convert_kwargs_to_snake_case
def resolve_anarticle_categories(obj, info, **kwargs):
    name = kwargs.get('name', '')
    description = kwargs.get('description', '')

    queryset = []
    filters = []

    if name:
        filters.append(Q(name__icontains=name))

    if description:
        filters.append(Q(description__icontains=description))

    if filters:
        queryset = obj.filter(reduce(operator.and_, filters)) \
                if isinstance(obj, QuerySet) \
                else Category.objects.filter(reduce(operator.and_, filters))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else Category.objects.all()

    return queryset


anarticle = NodeObjectType('AnArticle')
anarticle_paragraph = ObjectType('AnArticleParagraph')


@anarticle.instance_resolver
def resolve_anarticle_instance(id, *_):
    return Article.objects.get(id=id)


@anarticle.field('paragraphs')
def resolve_anarticle_paragraphs(obj, *_):
    return obj.paragraph_set.all()


@anarticle.connection('tags')
def resolve_anarticle_tag_connection(obj, info, **kwargs):
    return resolve_anarticle_tags(obj.tags.all(), info, kwargs)


@convert_kwargs_to_snake_case
def resolve_anarticles(obj, info, **kwargs):
    is_published = kwargs.get('is_published', None)
    published_at = kwargs.get('published_at', timezone.now())
    tags = kwargs.get('tags', '')
    title = kwargs.get('title', '')

    queryset = []
    filters = [
        Q(published_at__lt=published_at)
    ]

    if is_published is not None:
        filters.append(Q(is_published=is_published))

    if tags:
        values = [t.strip() for t in tags.split(',')]
        filters.append(Q(tags__name__in=values))

    if title:
        filters.append(Q(title__icontains=title))

    queryset = obj.filter(reduce(operator.and_, filters)) \
        if isinstance(obj, QuerySet) \
        else Article.objects.filter(reduce(operator.and_, filters))

    return queryset


types = [anarticle, anarticle_paragraph, anarticle_tag, anarticle_category]
