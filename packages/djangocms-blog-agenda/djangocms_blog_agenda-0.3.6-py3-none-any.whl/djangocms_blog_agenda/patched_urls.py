from django.urls import path
from django.utils.translation import pgettext_lazy
from djangocms_blog.urls import urlpatterns as original_patterns

from .views import (
    AgendaAndPostListView,
    AgendaCategoryEntriesView,
    AgendaPreviousEventsListView,
    AgendaTaggedListView,
)


# Here are the patched urls that still includes the original urlpattern of djangocms_blog.
# But it also adds an AgendaAndPostListView (that replace the original PostListView).

urlpatterns = [
    path(
        pgettext_lazy("agenda_view_url", "archives/"),
        AgendaPreviousEventsListView.as_view(),
        name="agenda-previous-events",
    ),
    path("", AgendaAndPostListView.as_view(), name="agenda-coming-soon"),
    path(
        "category/<str:category>/",
        AgendaCategoryEntriesView.as_view(),
        name="agenda-posts-category",
    ),
    path("tag/<slug:tag>/", AgendaTaggedListView.as_view(), name="posts-tagged"),
    *original_patterns,
]
