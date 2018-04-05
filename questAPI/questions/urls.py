from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import IndexView, QuestionView, \
#     QuestionnaireView,DetailedQuestionView,DetailedQuestionnaireView,\
#     DetailedQuestionHtmlView, DetailedQuestionnaireHtmlView, LemmaSortCode
from .views import *

urlpatterns = {
    url(r'^$', IndexView.as_view()),
    url(r'^ontology/?$', OntologyView.as_view()),
    url(r'^question/?$', QuestionView.as_view()),
    url(r'^question/(?P<pk>[0-9]+[-][A-Z]+[0-9]+)/?$', DetailedQuestionView.as_view()),
    url(r'^questionnaire/?$', QuestionnaireView.as_view()),
    url(r'^questionnaire/(?P<pk>[0-9]+)/?$', DetailedQuestionnaireView.as_view()),
    # here details of the data being viewed as html
    url(r'^question/(?P<pk>[0-9]+[-][A-Z]+[0-9]+).html/?$', DetailedQuestionHtmlView.as_view()),
    url(r'^questionnaire/(?P<pk>[0-9]+).html/?$', DetailedQuestionnaireHtmlView.as_view()),

    url(r'^lemmaSort/(?P<entry>[\w\-]+)$', LemmaSortCode.as_view()),
    url(r'^lem:qmaSortBatch/(?P<entry>[{][\w\-]+[}])$', LemmaSortCode.as_view()),

}

urlpatterns = format_suffix_patterns(urlpatterns)
