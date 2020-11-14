from src import utils

from django.core.exceptions import ValidationError


def validate_header_image(wide_image: object):
    """Validates image of the header."""
    if not utils.image_size_match(wide_image, width=1920, height=720):
        raise ValidationError('The image must be 1920x720')


def validate_post_image(normal_image: object):
    """Validates image of the post."""
    if not utils.image_size_match(normal_image, width=1200, height=800):
        raise ValidationError('The image must be 1200x800')


def validate_category_tag_image(normal_image: object):
    """Validates image of the category and tag."""
    if not utils.image_size_match(normal_image, width=1920, height=480):
        raise ValidationError('The image must be 1920x480')
