from django.db.models import Q
from django.utils import timezone
from djangocms_blog.views import (
    CategoryEntriesView,
    PostDetailView,
    PostListView,
    TaggedListView,
)


class AgendaDetailView(PostDetailView):
    ...


class AgendaComingEventsMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if "agenda" in self.config.template_prefix:
            return qs.order_by("extension__event_start_date").filter(
                (
                    Q(extension__event_end_date__isnull=True)
                    & Q(extension__event_start_date__gte=timezone.now())
                )
                | (
                    Q(extension__event_end_date__isnull=False)
                    & Q(extension__event_end_date__gte=timezone.now())
                )
            )
        return qs


class AgendaAndPostListView(AgendaComingEventsMixin, PostListView):
    ...


class AgendaCategoryEntriesView(AgendaComingEventsMixin, CategoryEntriesView):
    ...


class AgendaTaggedListView(AgendaComingEventsMixin, TaggedListView):
    ...


class AgendaPreviousEventsListView(PostListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("-extension__event_start_date").filter(
            (
                Q(extension__event_end_date__isnull=True)
                & Q(extension__event_start_date__lt=timezone.now())
            )
            | (
                Q(extension__event_end_date__isnull=False)
                & Q(extension__event_end_date__lt=timezone.now())
            )
        )
