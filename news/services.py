from django.db.models import F, Q

from news.models import PostModel, PinnedPostModel, PostCategoryModel, PostTagModel, PostViewsModel
from settings.models import SiteContactsModel
from users.models import UserModel


def get_site_settings():
    """Returns main settings of site."""
    return SiteContactsModel.objects.first()


def get_previous_post(post: object):
    """Returns the previous published post."""
    return PostModel.objects.filter(created_at__lt=post.created_at, is_published=True).first()


def get_next_post(post: object):
    """Returns the next published post."""
    return PostModel.objects.filter(created_at__gt=post.created_at, is_published=True).last()


def get_pinned_post_list():
    """Returns list of published pinned posts."""
    return PinnedPostModel.objects \
        .filter(pinned_post__is_published=True) \
        .select_related('pinned_post__author', 'pinned_post__category')


def get_recent_post_list(end: int):
    """Returns list of published recent posts without pinned posts."""
    pinned_post_list = get_pinned_post_list()
    return PostModel.objects.exclude(pinned_posts__in=pinned_post_list) \
        .filter(is_published=True)[:end] \
        .select_related('author', 'category')


def get_post_list(start: int):
    """Returns list of published posts without pinned posts and without recent posts."""
    pinned_post_list = get_pinned_post_list()
    return PostModel.objects.exclude(pinned_posts__in=pinned_post_list) \
        .filter(is_published=True)[start:] \
        .select_related('author', 'category')


def get_post_by_slug(slug: str):
    """Returns published post by slug."""
    return PostModel.objects.filter(slug=slug, is_published=True) \
        .select_related('author', 'category').prefetch_related('tags')


def get_post_by_category(slug: str):
    """Returns list of published posts by category."""
    return PostModel.objects.filter(category__slug=slug, is_published=True) \
        .select_related('author', 'category')


def get_post_by_tag(slug: str):
    """Returns list of published posts by tag."""
    return PostModel.objects.filter(tags__slug=slug, is_published=True) \
        .select_related('author', 'category')


def get_post_slug_by_pk(pk: int):
    """Returns post by pk."""
    return PostModel.objects.get(pk=pk).slug


def get_post_by_author(slug: str):
    """Returns list of published posts by author."""
    return PostModel.objects.filter(author__username=slug, is_published=True) \
        .select_related('author', 'category')


def get_author_by_slug(slug: str):
    """Returns an author of published posts by slug."""
    return UserModel.objects.filter(username=slug).first()


def get_category_by_slug(slug: str):
    """Returns a category by slug."""
    return PostCategoryModel.objects.filter(slug=slug).first()


def get_tag_by_slug(slug: str):
    """Returns a tag by slug."""
    return PostTagModel.objects.filter(slug=slug).first()


def update_number_field(obj: object, field: str, value: int, ip: str):
    """Update wanted field of database."""
    if not PostViewsModel.objects.filter(ip=ip, post=obj).exists():
        obj.views = F(field) + value
        obj.save(update_fields=[field])
        obj.refresh_from_db()
        PostViewsModel.objects.create(ip=ip, post=obj)


def get_post_list_by_search_filter(search_input: str):
    """Returns list of published posts where search input exists in title or content."""
    return PostModel.objects.filter(
            Q(title__icontains=search_input) |
            Q(content__icontains=search_input),
            is_published=True
        ).select_related('author', 'category')


def get_list_published_posts():
    """Returns list of published posts."""
    return PostModel.objects.filter(is_published=True) \
        .select_related('author', 'category').prefetch_related('tags')


def get_related_post_list(current_post: object):
    """"Returns list of 3 related published posts using matches of current post tags with the others posts."""
    current_post_tag_list = current_post.tags.all()
    post_list = get_list_published_posts().exclude(pk=current_post.id)

    related_post_list = []
    related_post_matches_dict = {}

    # Put format "post: count" into "related_post_matches_dict" dictionary
    # where "count" - total matches of "current_post" with iteration "post"
    for post in post_list:
        post_tag_list = post.tags.all()
        matches = len(set(current_post_tag_list) & set(post_tag_list))
        related_post_matches_dict[post] = matches

    # Returns dictionary as first three rows with max "count" value
    related_post_matches_dict = sorted(related_post_matches_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    for related_post in related_post_matches_dict:
        related_post_list.append(related_post[0])
    return related_post_list
