from django.urls import path

from .views import *


urlpatterns = [
    path('author/<slug:slug>/', PostAuthorView.as_view(), name='author'),
    path('category/<slug:slug>/', PostCategoryView.as_view(), name='category'),
    path('posts/<slug:slug>/', PostView.as_view(), name='posts'),
    path('tag/<slug:slug>/', PostTagView.as_view(), name='tag'),
    path('about/', site_about_view, name='about'),
    path('contacts/', SiteContactsView.as_view(), name='contacts'),
    path('search/', SearchPostView.as_view(), name='search'),
    path('', PostListView.as_view(), name='home'),
]
