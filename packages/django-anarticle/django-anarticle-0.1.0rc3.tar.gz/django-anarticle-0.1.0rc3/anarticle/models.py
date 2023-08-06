"""
Copyright (c) 2014-present, aglean Inc.
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from .utils import image_path, image_url


class Tag(models.Model):
    # detail
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=image_path,
        help_text=(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return image_url(self)

    @property
    def article_count(self):
        return self.article_set.filter(is_published=True).count()


class Category(models.Model):
    # relationship
    tags = models.ManyToManyField(Tag)

    # detail
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=image_path,
        help_text=(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return image_url(self)

    @property
    def tag_count(self):
        return self.tags.count()


class Article(models.Model):
    # relationship
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True)

    # detail
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        help_text=(
            'Characters combine with numbers, underscores or hyphens.'
            'Ex: today1_news-headline'
        ),
        allow_unicode=True,
        blank=True
    )
    summary = models.TextField()
    image = models.ImageField(
        upload_to=image_path,
        help_text=(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    # flag
    is_published = models.BooleanField(
        'Published',
        help_text=('Designates whether the item is published on the site.'),
        default=True
    )

    # datetime
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return image_url(self)


@receiver(pre_save, sender=Article)
def post_article_process(sender, instance, **kwargs):

    if instance.is_published and instance.published_at is None:
        instance.published_at = timezone.now()

    if not instance.slug.strip():
        instance.slug = slugify(instance.title, allow_unicode=True)


class Paragraph(models.Model):
    # relationship
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    # detail
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=image_path,
        help_text=(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )
    image_text = models.CharField(
        max_length=255,
        help_text='Descripe the image content',
        blank=True
    )

    @property
    def image_url(self):
        return image_url(self)
