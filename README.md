# ACDH Semantic Web


This repository contains applications and services to support semantic enrichment of historical and socio-cultural datat.
### The Questionnaire

The questionnaire provides access to the linked open data of the questionnaire collection.

Questionnaire Data:

The semantic data of the questionnaire is available in as nquad format here (location). After running the app, to upload the data to jena fuseki,

1. Download the dataset (questionnaire.nq)
2. Go to http://localhost:3030/ (The database password is available from the docker-compose.yml file)
3. navigate to manage datasets,
4. Upload the data with adataset name "Questionnaire"

Questionnaire API:

The api returns a JSON file of the RDF triples. Currently, four endpoints are available:

1. to get all questionnaires (http://localhost:8000/questionnaire/questionnaire)
2. to get a specificv questionnaire by its id (http://localhost:8000/questionnaire/questionnaire/id) . Currently there are 120 questionnaires.
3. to get all questions (http://localhost:8000/questionnaire/question)
4. to get a specific question by its id (http://localhost:8000/questionnaire/question/id). Note that the format of the id is (one or more digit followed by hyphen followed by Capital letter followed by one or more digit)
eg. "1-A10"



### Collaboration

Project is open source and anybody can contribute. Please use issue tracking. Create branches for each issue and submit PRs.
