"""
Copyright (c) 2014-present, aglean Inc.
"""
import pytest

from anarticle.models import Tag, Category, Article
from anarticle.resolvers import resolve_anarticle_tags, \
        resolve_anarticle_categories, resolve_anarticles


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        tag_1 = Tag.objects.create(name='red')
        tag_2 = Tag.objects.create(name='black')
        tag_3 = Tag.objects.create(name='white')

        cat_1 = Category.objects.create(name='sun', description='day')
        cat_2 = Category.objects.create(name='moon', description='day')

        cat_1.tags.add(tag_1)
        cat_2.tags.add(tag_2, tag_3)

        art_1 = Article.objects.create(title='red sun', summary='sum raise')
        art_2 = Article.objects.create(title='white moon', summary='moon light')

        art_1.tags.add(tag_1)
        art_2.tags.add(tag_2, tag_3)


class TestTag:
    @pytest.mark.django_db
    def test_reoslve_tags_from_root_without_args(self):
        assert resolve_anarticle_tags(None, None).count() == 3

    @pytest.mark.django_db
    def test_reoslve_tags_from_root_with_args(self):
        assert resolve_anarticle_tags(None, None, name='ack').count() == 1

    def test_resolve_tags_from_obj_without_args(self, mocker):
        queryset = mocker.patch('anarticle.models.Tag.objects.all')
        queryset.return_value = queryset
        queryset.count.return_value = 0
        assert resolve_anarticle_tags(queryset, None).count() == 0

    def test_resolve_tags_from_obj_with_args(self, mocker):
        queryset = mocker.patch('anarticle.models.Tag.objects.filter')
        queryset.return_value = queryset
        queryset.count.return_value = 0
        assert resolve_anarticle_tags(queryset, None, name='test').count() == 0


class TestCategory:
    @pytest.mark.django_db
    def test_reoslve_categories_from_root_without_args(self):
        assert resolve_anarticle_categories(None, None).count() == 2

    @pytest.mark.django_db
    def test_reoslve_categories_from_root_with_args(self):
        assert resolve_anarticle_categories(None,
                                            None,
                                            name='su',
                                            description='da').count() == 1

    def test_resolve_categories_from_obj_without_args(self, mocker):
        queryset = mocker.patch('anarticle.models.Category.objects.all')
        queryset.return_value = queryset
        queryset.count.return_value = 1
        assert resolve_anarticle_categories(queryset, None).count() == 1

    def test_resolve_categories_from_obj_with_args(self, mocker):
        queryset = mocker.patch('anarticle.models.Category.objects.filter')
        queryset.return_value = queryset
        queryset.count.return_value = 1
        assert resolve_anarticle_categories(queryset,
                                            None,
                                            name='test',
                                            description='test').count() == 1


class TestArticle:
    @pytest.mark.django_db
    def test_reoslve_articles_from_root_without_args(self):
        assert resolve_anarticles(None, None).count() == 2

    @pytest.mark.django_db
    def test_reoslve_articles_from_root_with_args(self):
        assert resolve_anarticles(None,
                                  None,
                                  title="moon",
                                  tags='red,white').count() == 1

    def test_resolve_articles_from_obj_without_args(self, mocker):
        queryset = mocker.patch('anarticle.models.Article.objects.filter')
        queryset.return_value = queryset
        queryset.count.return_value = 2
        assert resolve_anarticles(queryset, None).count() == 2

    def test_resolve_articles_from_obj_with_args(self, mocker):
        queryset = mocker.patch('anarticle.models.Article.objects.filter')
        queryset.return_value = queryset
        queryset.count.return_value = 2
        assert resolve_anarticles(queryset,
                                  None,
                                  tags='black,white').count() == 2
