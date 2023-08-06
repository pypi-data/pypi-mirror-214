"""
Copyright (c) 2014-present, aglean Inc.
"""
from ariadne import ObjectType
from ariadne_relay import NodeObjectType
from asgiref.sync import sync_to_async

from .models import Article, Tag, Category
from .bindables import resolve_anarticle_tags, resolve_anarticles
from .bindables_sync import resolve_anarticle_tags_sync, \
        resolve_anarticles_sync


anarticle_tag = NodeObjectType('AnArticleTag')
anarticle_category = NodeObjectType('AnArticleCategory')
anarticle = NodeObjectType('AnArticle')
anarticle_paragraph = ObjectType('AnArticleParagraph')


async def resolve_anarticle_tag_instance(id, *_):
    return await Tag.objects.aget(id=id)


async def resolve_anarticle_tag_articles_connection(obj,
                                                    info,
                                                    connection_args,
                                                    **kwargs):
    """resolve tag connection to articles"""
    articles = await sync_to_async(obj.article_set.all)()
    return await resolve_anarticles(articles, info, connection_args, kwargs)


async def resolve_anarticle_category_instance(id, *_):
    return await Category.objects.aget(id=id)


async def resolve_anarticle_category_tags_connection(obj,
                                                     info,
                                                     connection_args,
                                                     **kwargs):
    """resolve category connection to tags"""
    tags = await sync_to_async(obj.tags.all)()
    return await resolve_anarticle_tags(tags, info, connection_args, kwargs)


async def resolve_anarticle_instance(id, *_):
    return await Article.objects.aget(id=id)


async def resolve_anarticle_paragraphs(obj, *_):
    return await sync_to_async(obj.paragraph_set.all)()


async def resolve_anarticle_tags_connection(obj, info, connection_args,
                                            **kwargs):
    """resolve article connection to tags"""
    tags = await sync_to_async(obj.tags.all)()
    return resolve_anarticle_tags(tags, info, connection_args, kwargs)


def resolve_anarticle_tag_instance_sync(id, *_):
    return Tag.objects.get(id=id)


def resolve_anarticle_tag_articles_connection_sync(obj, info, connection_args,
                                                   **kwargs):
    """sync resolve tag connection to articles"""
    return resolve_anarticles_sync(obj.article_set.all(), info,
                                   connection_args, kwargs)


def resolve_anarticle_category_instance_sync(id, *_):
    return Category.objects.get(id=id)


def resolve_anarticle_category_tags_connection_sync(obj,
                                                    info,
                                                    connection_args,
                                                    **kwargs):
    """sync resolve category connection to tags"""
    return resolve_anarticle_tags_sync(obj.tags.all(), info, connection_args,
                                       kwargs)


def resolve_anarticle_instance_sync(id, *_):
    return Article.objects.get(id=id)


def resolve_anarticle_paragraphs_sync(obj, *_):
    return obj.paragraph_set.all()


def resolve_anarticle_tags_connection_sync(obj, info, connection_args,
                                           **kwargs):
    """sync resolve article connection to tags"""
    return resolve_anarticle_tags_sync(obj.tags.all(), info, connection_args,
                                       kwargs)
