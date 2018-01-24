from rest_framework import generics
from .serializers import QuestionlistSerializer, questSerializer
from .models import Questionlist
from .models import answers
from SPARQLWrapper import SPARQLWrapper, JSON
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import requests


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Questionlist.objects.all()
    serializer_class = QuestionlistSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Questionlist.objects.all()
    serializer_class = QuestionlistSerializer

class QuestView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper("http://fuseki:3030/questionnaire/query")
        sparql.setQuery("""
                   # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    # SELECT ?s ?label
                    # WHERE { ?s rdfs:label ?label } limit 10

                    select distinct ?subject ?predicate ?object
                    where {?subject ?predicate ?object} LIMIT 10
                """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class QuestDetailView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper("http://fuseki:3030/questionnaire/query")
        sparql.setQuery("""
                     # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     # SELECT ?s ?label
                            # WHERE { ?s rdfs:label ?label } limit 10

                    select distinct ?subject ?predicate ?object
                    where {?subject ?predicate ?object} LIMIT 10
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)




                # def quest(request):
#     print("reached here")
#
#     sparql = SPARQLWrapper("http://fuseki:3030/questionnaire/query")
#     sparql.setQuery("""
#         # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#          # SELECT ?s ?label
#          # WHERE { ?s rdfs:label ?label } limit 10
#
#          select distinct ?subject ?predicate ?object
#          where {?subject ?predicate ?object} LIMIT 10
#      """)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     results = JSONRenderer().render(results)
#
#     template = loader.get_template('questions/quests.html')
#     context = {'result': results,
#                }
#
#     return HttpResponse(template.render(context, request))