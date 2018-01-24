from django.conf import settings
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView
from .views import DetailsView
from .views import QuestView

urlpatterns = {
    url(r'^questionlists/$', CreateView.as_view(), name="create"),
    url(r'^questionlists/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
    url(r'^quest/$', QuestView.as_view()),
    url(r'^quest/(?P<pk>[0-9]+)/$', QuestView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]