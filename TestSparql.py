from django.db import models
from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    # SELECT ?s ?label
    # WHERE { ?s rdfs:label ?label } limit 10
    
    select distinct ?s ?Concept 
    where {?s a ?Concept} LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"])