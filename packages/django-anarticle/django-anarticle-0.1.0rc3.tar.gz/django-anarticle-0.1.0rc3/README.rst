====================================
django app of an article
====================================

Anarticle uses tag, catelog, and article models to publish articles.
Support for Ariadne graphQL with pre-defined types and basic resolvers.

------------
Requirements
------------

* Python 3.10+
* django 4.0+
* pillow 9.4.0+

--------
Settings
--------

Store uploaded file with tokenize file name, default to False

* ANARTICLE_USE_TOKEN_FILENAME = True

-------------------
Django admin mixins
-------------------

Use predefined mixins to construct the admin class.

* TagAdminMixin
* CategoryAdminMixin
* ArticleAdminMixin

.. code:: python

    from django.contrib import admin

    from anarticle.models import Tag
    from anarticle.admin.mixins import TagAdminMixin


    @admin.register(Tag)
    class TagAdmin(TagAdminMixin, ModelAdmin):
        ...

---------------------------
Ariadne types and resolvers
---------------------------

Integrate predefined types and resolvers to scheme.

Requirements
------------

* ariadne 0.16.0+
* ariadne-relay 0.1.0a8+

**scheme**

.. code:: python

   from anarticle.graphqls import anarticle_schema


* anarticle/graphqls/article.graphql
* anarticle/graphqls/tag.graphql
* anarticle/graphqls/category.graphql

**types**

.. code:: python

   from anarticle.graphqls import anarticle_bindables


* anarticle
* anarticle_paragraph
* anarticle_tag
* anarticle_category

**resolvers**

Async version

.. code:: python

   from anarticle.graphqls import resolve_anarticle_tag_instance, \
           resolve_anarticle_tag_articles_connection, resolve_anarticle_tags

   anarticle_tag.set_instance_resolver(resolve_anarticle_tag_instance)
   anarticle_tag.set_connection('articles', resolve_anarticle_tag_articles_connection)

   query.set_field('tags', resolve_anarticle_tags)


* resolve_anarticle_tag_instance,
* resolve_anarticle_tag_articles_connection,
* resolve_anarticle_category_instance,
* resolve_anarticle_category_tags_connection,
* resolve_anarticle_instance,
* resolve_anarticle_paragraphs,
* resolve_anarticle_tags_connection,
* resolve_anarticle_tags,
* resolve_anarticle_categories,
* resolve_anarticles,


Sync version

* resolve_anarticle_tag_instance_sync,
* resolve_anarticle_tag_articles_connection_sync,
* resolve_anarticle_category_instance_sync,
* resolve_anarticle_category_tags_connection_sync,
* resolve_anarticle_instance_sync,
* resolve_anarticle_paragraphs_sync,
* resolve_anarticle_tags_connection_sync,
* resolve_anarticle_tags_sync,
* resolve_anarticle_categories_sync,
* resolve_anarticles_sync,

-------
License
-------

django-anarticle is released under the terms of **Apache license**. Full details in LICENSE file.
