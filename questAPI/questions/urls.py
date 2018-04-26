from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import IndexView, QuestionView, \
#     QuestionnaireView,DetailedQuestionView,DetailedQuestionnaireView,\
#     DetailedQuestionHtmlView, DetailedQuestionnaireHtmlView, LemmaSortCode
from .views import *
from django.conf.urls.static import static

urlpatterns = {
    url(r'^$', IndexView.as_view()),
    url(r'^ontology/?$', OntologyView.as_view()),
    url(r'^Question/?$', QuestionView.as_view()),
    url(r'^Question/(?P<pk>[0-9]+[-][A-Z]+[0-9]+)/?$', DetailedQuestionView.as_view()),
    url(r'^Questionnaire/?$', QuestionnaireView.as_view()),
    url(r'^Questionnaire/(?P<pk>[0-9]+)/?$', DetailedQuestionnaireView.as_view()),
    # here details of the data being viewed as html
    url(r'^Question/(?P<pk>[0-9]+[-][A-Z]+[0-9]+).html/?$', DetailedQuestionHtmlView.as_view()),
    url(r'^Questionnaire/(?P<pk>[0-9]+).html/?$', DetailedQuestionnaireHtmlView.as_view()),

    url(r'^lemmaSort/(?P<entry>[\w\-]+)$', LemmaSortCode.as_view()),
    url(r'^lemmaSortBatch/(?P<entry>[{][\w\-]+[}])$', LemmaSortCode.as_view()),



    url(r'^Lemma/?$', LemmaView.as_view()),
    url(r'^Lemma/(?P<pk>[0-9]+)/?$', DetailedLemmaView.as_view()),

    url(r'^Source/?$', SourceView.as_view()),
    url(r'^Source/(?P<pk>[0-9]+)/?$', DetailedSourceView.as_view()),

    url(r'^PaperSlip/?$', PaperSlipView.as_view()),
    url(r'^PaperSlip/(?P<pk>[0-9]+)/?$', DetailedPaperSlipView.as_view()),

    url(r'^Multimedia/?$', MultimediaView.as_view()),
    url(r'^Multimedia/(?P<pk>[0-9]+)/?$', DetailedMultimediaView.as_view()),

    url(r'^PaperSlipRecord/?$', PaperSlipRecordView.as_view()),
    url(r'^PaperSlipRecord/(?P<pk>[0-9]+)/?$', DetailedPaperSlipRecordView.as_view()),

    url(r'^Person/?$', PersonView.as_view()),
    url(r'^Person/(?P<pk>[0-9]+)/?$', DetailedPersonView.as_view()),

}

urlpatterns = format_suffix_patterns(urlpatterns)
