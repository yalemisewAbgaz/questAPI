from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from SPARQLWrapper import SPARQLWrapper, JSON
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import ast
import os, os.path

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from django.core.paginator import Paginator
from django.conf import settings


dataset="http://fuseki:3030/dboe/query"


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
        template_name = "index.html"


class OntologyView(generic.TemplateView):
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
        sparql = SPARQLWrapper(dataset)
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
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/Questionnaire_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/Questionnaire_graph> {?s ?p ?o}
                    } Limit 100
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results=results['results']['bindings']
        return Response(results)


class QuestionView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/Question_graph>
                    WHERE {
                    Graph  <http://exploreat.adaptcentre.ie/Question_graph> {?s ?p ?o}
                    }
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class LemmaView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/Lemma_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/Lemma_graph> {?s ?p ?o}
                    } 
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class SourceView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/Source_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/Source_graph> {?s ?p ?o}
                    }
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class PaperSlipView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/PaperSlip_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/PaperSlip_graph> {?s ?p ?o}
                    } 
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class PaperSlipRecordView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph> {?s ?p ?o}
                    }
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class MultimediaView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/Multimedia_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/Multimedia_graph> {?s ?p ?o}
                    }
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class PersonView(APIView):
    def get(self, request):
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                    SELECT *
                    From named <http://exploreat.adaptcentre.ie/Person_graph>
                    WHERE {
                    Graph <http://exploreat.adaptcentre.ie/Person_graph> {?s ?p ?o}
                    } 
                 """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
# ==================================================
class DetailedQuestionnaireView(APIView):
    def get(self, request,pk):
        #the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj = "<http://exploreat.adaptcentre.ie/Questionnaire/" + pk + ">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/Questionnaire_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/Questionnaire_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedQuestionView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/Question/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/Question_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/Question_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        # if request.accepted_renderer.format == 'html':
        #     # TemplateHTMLRenderer takes a context dict,
        #     # and additionally requires a 'template_name'.
        #     # It does not require serialization.
        #     return Response(results, template_name='question.html')
        return Response(results)


class DetailedPaperSlipRecordView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/PaperSlipRecord/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedLemmaView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/Lemma/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/Lemma_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/Lemma_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)


class DetailedSourceView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/Source/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/Source_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/Source_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedPaperSlipView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/PaperSlip/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/PaperSlip_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/PaperSlip_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

    
class DetailedMultimediaView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/Multimedia/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/Multimedia_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/Multimedia_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedPersonView(APIView):
    def get(self, request,pk):
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        subj="<http://exploreat.adaptcentre.ie/Person/" +pk +">"
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                        SELECT *
                        From named <http://exploreat.adaptcentre.ie/Person_graph>
                        WHERE {
                        Graph <http://exploreat.adaptcentre.ie/Person_graph> {""" +subj + """ ?p ?o}
                        } 
                     """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
# ===================================================
class DetailedQuestionnaireViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                       
                        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                        SELECT *

                        From named <http://exploreat.adaptcentre.ie/Questionnaire_graph>
                        WHERE {
                                Graph <http://exploreat.adaptcentre.ie/Questionnaire_graph> {?s ?p ?o}.
                                {
                                    select distinct ?s{
                                    Graph <http://exploreat.adaptcentre.ie/Questionnaire_graph> 
                                     {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#Questionnaire>}.
                                 }
                                order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/Questionnaire/","")),">","")))
                                Limit""" + str(limit)  + """
                                OFFSET""" + str(offset) + """
                                }  
                        }
                         """
                     )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedQuestionViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/Question_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/Question_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/Question_graph>
                                             {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#Question>}.
                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/Question/","")),">","")))
                                        Limit""" + str(limit)  + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedPaperSlipRecordViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/PaperSlipRecord_graph> 
                                             {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#PaperSlipRecord>}.
                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/PaperSlipRecord/","")),">","")))
                                        Limit""" + str(limit) + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
class DetailedLemmaViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/Lemma_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/Lemma_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/Lemma_graph>
                                             {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#Lemma>}.   
                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/Lemma/","")),">","")))
                                        Limit""" + str(limit) + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
class DetailedSourceViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/Source_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/Source_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/Source_graph>  
                                            {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#Source>}.
                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/Source/","")),">","")))
                                        Limit""" + str(limit)  + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

class DetailedPaperSlipViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/PaperSlip_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/PaperSlip_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/PaperSlip_graph> 
                                             {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#PaperSlip>}.
                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/PaperSlip/","")),">","")))
                                        Limit""" + str(limit)  + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
class DetailedMultimediaViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/Multimedia_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/Multimedia_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/Multimedia_graph> 
                                             {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#Multimedia>}.
                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/Multimedia/","")),">","")))
                                        Limit""" + str(limit)  + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)
class DetailedPersonViewLimit(APIView):
    def get(self, request,limit,offset):
        if int(limit)>100:
            limit=100
        if int(offset)<0:
            offset=0
        # the query will strip the questionnaire number and replace http://localhost/oldca/fragebogen/1 in the query
        sparql = SPARQLWrapper(dataset)
        sparql.setQuery("""

                               
                                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                                SELECT *

                                From named <http://exploreat.adaptcentre.ie/Person_graph>
                                WHERE {
                                        Graph <http://exploreat.adaptcentre.ie/Person_graph> {?s ?p ?o}.
                                        {
                                            select distinct ?s{
                                            Graph <http://exploreat.adaptcentre.ie/Person_graph>  
                                            {?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://explorations4u.acdh.oeaw.ac.at/ontology/oldcan#author>}.

                                         }
                                        order by asc(xsd:integer(replace(str(replace(str(?s),"http://exploreat.adaptcentre.ie/Person/","")),">","")))
                                        Limit""" + str(limit) + """
                                        OFFSET""" + str(offset) + """
                                        }  
                                }
                                 """
                        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return Response(results)

#  =====================================

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





