"""
Copyright (c) 2014-present, aglean Inc.
"""
import operator
from functools import reduce

from asgiref.sync import sync_to_async
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone

from .models import Article, Tag, Category


async def resolve_anarticle_tags(obj, info, connection_args, **kwargs):
    name = kwargs.get('name', '')

    queryset = []
    lookups = []

    if name:
        lookups.append(Q(name__icontains=name))

    if lookups:
        queryset = await sync_to_async(obj.filter)(reduce(operator.and_,
                                                          lookups)) \
                if isinstance(obj, QuerySet) \
                else await sync_to_async(Tag.objects.filter)(
                        reduce(operator.and_, lookups)
                    )
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else await sync_to_async(Tag.objects.all)()

    return queryset


async def resolve_anarticle_categories(obj, info, connection_args, **kwargs):
    name = kwargs.get('name', '')
    description = kwargs.get('description', '')

    queryset = []
    lookups = []

    if name:
        lookups.append(Q(name__icontains=name))

    if description:
        lookups.append(Q(description__icontains=description))

    if lookups:
        queryset = await sync_to_async(obj.filter)(reduce(operator.and_,
                                                          lookups)) \
                if isinstance(obj, QuerySet) \
                else await sync_to_async(Category.objects.filter)(
                        reduce(operator.and_, lookups)
                    )
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else await sync_to_async(Category.objects.all)()

    return queryset


def resolve_anarticles(obj, info, connection_args, **kwargs):
    is_published = kwargs.get('is_published', None)
    published_at = kwargs.get('published_at', timezone.now())
    tags = kwargs.get('tags', '')
    title = kwargs.get('title', '')

    queryset = []
    lookups = [
        Q(published_at__lt=published_at)
    ]

    if is_published is not None:
        lookups.append(Q(is_published=is_published))

    if tags:
        values = [t.strip() for t in tags.split(',')]
        lookups.append(Q(tags__name__in=values))

    if title:
        lookups.append(Q(title__icontains=title))

    queryset = sync_to_async(obj.filter)(reduce(operator.and_, lookups)) \
        if isinstance(obj, QuerySet) \
        else await (Article.objects.filter)(reduce(operator.and_, lookups))

    return queryset
