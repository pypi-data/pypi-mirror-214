"""
Copyright (c) 2014-present, aglean Inc.
"""
from ariadne import load_schema_from_path

from .type_defs import (
    anarticle_tag,
    anarticle_category,
    anarticle,
    anarticle_paragraph,
    resolve_anarticle_tag_instance,
    resolve_anarticle_tag_articles_connection,
    resolve_anarticle_category_instance,
    resolve_anarticle_category_tags_connection,
    resolve_anarticle_instance,
    resolve_anarticle_paragraphs,
    resolve_anarticle_tags_connection,
    resolve_anarticle_tag_instance_sync,
    resolve_anarticle_tag_articles_connection_sync,
    resolve_anarticle_category_instance_sync,
    resolve_anarticle_category_tags_connection_sync,
    resolve_anarticle_instance_sync,
    resolve_anarticle_paragraphs_sync,
    resolve_anarticle_tags_connection_sync,
)
from .bindables import (
    resolve_anarticle_tags,
    resolve_anarticle_categories,
    resolve_anarticles
)
from .bindables_sync import (
    resolve_anarticle_tags_sync,
    resolve_anarticle_categories_sync,
    resolve_anarticles_sync
)


anarticle_schema = load_schema_from_path('anarticle/graphqls')

anarticle_bindables = [anarticle_tag, anarticle_category, anarticle,
                       anarticle_paragraph]


__all__ = [
    'anarticle_scheme',
    'anarticle_bindables',
    resolve_anarticle_tag_instance,
    resolve_anarticle_tag_articles_connection,
    resolve_anarticle_category_instance,
    resolve_anarticle_category_tags_connection,
    resolve_anarticle_instance,
    resolve_anarticle_paragraphs,
    resolve_anarticle_tags_connection,
    resolve_anarticle_tags,
    resolve_anarticle_categories,
    resolve_anarticles,
    resolve_anarticle_tag_instance_sync,
    resolve_anarticle_tag_articles_connection_sync,
    resolve_anarticle_category_instance_sync,
    resolve_anarticle_category_tags_connection_sync,
    resolve_anarticle_instance_sync,
    resolve_anarticle_paragraphs_sync,
    resolve_anarticle_tags_connection_sync,
    resolve_anarticle_tags_sync,
    resolve_anarticle_categories_sync,
    resolve_anarticles_sync,
]
