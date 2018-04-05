from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from SPARQLWrapper import SPARQLWrapper, JSON
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import ast
import os, os.path
from django.conf import settings



def generateSortCode(currentLemma, sortEncodingDict):
    lemmaSortCode = ""
    currentLemma = prepareLemmaInOrder(currentLemma)
    # print("\nfinal conversion", currentLemma)
    for letter in currentLemma:
        if letter != ' ' or letter != '-':
            # print("the code for ", letter, " is ", sortEncodingDict[letter])
            if letter in sortEncodingDict:
                lemmaSortCode += sortEncodingDict[letter]
            else:  # for unknown characters such as  and special characters such as +,? and others used in the data
                lemmaSortCode += ''
    return lemmaSortCode


def prepareLemmaInOrder(rawLemma):
    inBracket = ""
    withBracket = ""
    beforeBracket = ""
    head = ""
    invertedHead = ""
    invertedInBraket = ""
    invertedBeforeBraket = ""

    if '(' in rawLemma and ')' in rawLemma:
        indexStart = rawLemma.find('(')
        indexEnd = rawLemma.find(')')
        inBracket = rawLemma[indexStart + 1: indexEnd]
        withBracket = rawLemma[indexStart: indexEnd + 1]
        beforeBracket = rawLemma[0:indexStart]
    head = rawLemma.replace(beforeBracket + withBracket, "")

    # print("The head = ", head)

    if '-' in head:
        indexAt = head.find('-')
        # If the - occurs in the middle of the head word, split the head word using - and reorder the compound word elements
        if indexAt > 0:
            compounds = head.split('-')
            for compound in compounds:
                invertedHead = compound + invertedHead
        else:
            invertedHead = head
    else:
        # if - doesn't appear anywhere, take it as it is
        invertedHead = head

    # Apply the same logic for the lemma in the bracket as the one used for the headword
    if '-' in beforeBracket:
        indexAt = beforeBracket.find('-')
        if indexAt > 0:
            compounds = beforeBracket.split('-')
            for compound in compounds:
                invertedBeforeBraket = compound + invertedBeforeBraket
        else:
            invertedBeforeBraket = beforeBracket
    else:
        invertedBeforeBraket = beforeBracket

    # Apply the same logic for the lemma in the bracket as the one used for the headword
    if '-' in inBracket:
        indexAt = inBracket.find('-')
        if indexAt > 0:
            compounds = inBracket.split('-')
            for compound in compounds:
                invertedInBraket = compound + invertedInBraket
        else:
            invertedInBraket = inBracket
    else:
        invertedInBraket = inBracket

    return invertedHead + invertedInBraket + invertedBeforeBraket


class IndexView(generic.TemplateView):
    def get(self, request):
        template_name = "index.html"

        
class OntologyView(generic.TemplateView):
    def get(self, request):
        template_name = "Ontology.owl"


class DetailedQuestionnaireHtmlView(generic.TemplateView):
    def get(self, request):
        template_name = "questionnaire.html"


class DetailedQuestionHtmlView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='question.html'
    def get(self, request, pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://localhost/oldca/frage/" +pk +">"
        sparql = SPARQLWrapper("http://fuseki:3030/Questionnaire/query")
        sparql.setQuery("""

                        SELECT *
                        From named <http://localhost/questions>
                        WHERE {
                        Graph <http://localhost/questions> {""" +subj + """ ?p ?o}
                        } Limit 50
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class QuestionnaireView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper("http://fuseki:3030/Questionnaire/query")
        sparql.setQuery("""

                    SELECT *
                    From named <http://localhost/questionnaires>
                    WHERE {
                    Graph <http://localhost/questionnaires> {?s ?p ?o}
                    } Limit 50
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
class QuestionView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper("http://fuseki:3030/Questionnaire/query")
        sparql.setQuery("""

                    SELECT *
                    From named <http://localhost/questions>
                    WHERE {
                    Graph <http://localhost/questions> {?s ?p ?o}
                    } Limit 50
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedQuestionnaireView(APIView):
    def get(self, request,pk):
        #the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj = "<http://localhost/oldca/fragebogen/" + pk + ">"
        sparql = SPARQLWrapper("http://fuseki:3030/Questionnaire/query")
        sparql.setQuery("""

                        SELECT *
                        From named <http://localhost/questionnaires>
                        WHERE {
                        Graph <http://localhost/questionnaires> {""" +subj + """ ?p ?o}
                        } Limit 50
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedQuestionView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://localhost/oldca/frage/" +pk +">"
        sparql = SPARQLWrapper("http://fuseki:3030/Questionnaire/query")
        sparql.setQuery("""

                        SELECT *
                        From named <http://localhost/questions>
                        WHERE {
                        Graph <http://localhost/questions> {""" +subj + """ ?p ?o}
                        } Limit 50
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        # if request.accepted_renderer.format == 'html':
        #     # TemplateHTMLRenderer takes a context dict,
        #     # and additionally requires a 'template_name'.
        #     # It does not require serialization.
        #     return Response(results, template_name='question.html')
        return Response(results)
class LemmaSortCode(APIView):
    def get(self, request,entry):

        lemmaRec=entry
        # This method prepares the raw lemma into a proper order. If a raw lemma appears as (ein-hin)pȧssen, it will convert it
        # to the head word first i.e pȧssen and convert all the compounds from right first to left  last i.e hin-ein. Hyphen, space and brackets
        # are not converted
        counter = 0
        records = set()
        # Read the sort key from a file================================
        print(settings.STATIC_URL)
        staticFileDir=os.path.join(settings.BASE_DIR, 'static')
        sortFiledir = os.path.join(staticFileDir, 'sortEncoding.txt')
        sortFile=open(sortFiledir, 'r')

        sortEncoding = sortFile.read()
        sortEncodingDict = ast.literal_eval(sortEncoding)


        if lemmaRec != "":
            content = str.split(lemmaRec.strip(), "\t")
            lemma = content[0]
            # print("current content of lemma ", lemma)
            if len(content) > 1:
                sortOriginal = content[1]
            else:
                sortOriginal = "Empty"
            print("\n\nRaw Input", lemmaRec)
            sortNew = generateSortCode(lemma.replace(" © 2008-2080 jost nickel", ""), sortEncodingDict)

        print("==>", lemma, sortOriginal, " \tnew\t", sortNew, sortOriginal == sortNew)
        result={'lemma':lemmaRec, 'sortCode':sortNew}
        return Response(result)





