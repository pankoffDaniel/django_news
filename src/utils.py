import os
import pytils
from pytils.translit import slugify

from django.utils.safestring import mark_safe
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _


def get_image(image: object, width='', height='', alt='') -> str:
    """Shows image in admin form."""
    if image:
        return mark_safe(f'<img src="{image.url}" width="{width}" height="{height}" alt="{alt}">')
    return _('No image')


def set_slug(title: str, slug: str) -> str:
    """If slug field is empty then slug is being set automatically and translit it in english."""
    if not slug:
        slug = pytils.translit.translify(title)
        slug = slugify(slug)
    return slug


def staff_action_message(row_update: int) -> str:
    """Message for staff in admin panel after some action."""
    if row_update == 1:
        message = '1 row was updated'
    else:
        message = f'{row_update} rows were updated'
    return message


def image_size_match(image: object, width: int, height: int) -> bool:
    """Returns a bool value if real size matches with wanted size."""
    real_width, real_height = get_image_dimensions(image)
    if real_width == width and real_height == height:
        return True
    return False


def get_post_upload_path(instance: object, filename: str) -> str:
    """Returns dynamic path to uploaded post images."""
    return os.path.join('images', 'posts', instance.title, filename)


def get_category_upload_path(instance: object, filename: str) -> str:
    """Returns dynamic path to uploaded category image."""
    return os.path.join('images', 'categories', instance.title, filename)


def get_tag_upload_path(instance: object, filename: str) -> str:
    """Returns dynamic path to uploaded tag image."""
    return os.path.join('images', 'tags', instance.title, filename)
