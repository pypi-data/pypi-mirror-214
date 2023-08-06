"""
Copyright (c) 2014-present, aglean Inc.
"""
from pathlib import PurePath
from secrets import token_urlsafe

from django.conf import settings
from django.utils import timezone


def image_path(instance, filename):
    fixed_filename = PurePath(filename).stem[:8] \
            if len(PurePath(filename).stem) > 8 else PurePath(filename).stem

    cleaned_filename = (
        f"{timezone.now().strftime('%Y%m%d%H%M%S%f')}-"
        f'{fixed_filename}{PurePath(filename).suffix}'
    )

    if getattr(settings, 'ANARTICLE_USE_TOKEN_FILENAME', False):
        return PurePath(instance._meta.app_label).joinpath(
                f'{token_urlsafe()}{PurePath(filename).suffix}')
    else:
        return PurePath(instance._meta.app_label).joinpath(cleaned_filename)


def image_url(instance):
    url = ''
    if instance.image:
        url = instance.image.url

    return url
