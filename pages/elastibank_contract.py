import os
import streamlit as st
from elasticsearch import Elasticsearch
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession, GenerationConfig, Image, Part

#WATCHOUT!!! For fine-tuning feature you need to import vertexai.preview instead of just vertexAI

# This page shows the integration with a fine-tuned text-bison model via VertexAI

# Code is presented for demo purposes but should not be used in production
# You may encounter exceptions which are not handled in the code


# Required Environment Variables
# gcp_project_id - Google Cloud project ID
# cloud_id - Elastic Cloud Deployment ID
# cloud_user - Elasticsearch Cluster User
# cloud_pass - Elasticsearch User Password

projid = os.environ['gcp_project_id']
cid = os.environ['cloud_id']
cp = os.environ['cloud_pass']
cu = os.environ['cloud_user']

generation_config = GenerationConfig(
    temperature=0.4, # 0 - 1. The higher the temp the more creative and less on point answers become
    max_output_tokens=2048, #modify this number (1 - 1024) for short/longer answers
    top_p=0.8,
    top_k=40,
    candidate_count=1,
)

vertexai.init(project=projid, location="us-central1")

model = GenerativeModel("gemini-pro")
visionModel = GenerativeModel("gemini-1.0-pro-vision-001")

# Connect to Elastic Cloud cluster
def es_connect(cid, user, passwd):
    es = Elasticsearch(cloud_id=cid, http_auth=(user, passwd))
    return es

# Search ElasticSearch index and return details on relevant products
def search_docs(query_text):

    # Elasticsearch query (BM25) and kNN configuration for hybrid search
    query = {
        "bool": {
            "must": [{
                "match": {
                    "title": {
                        "query": query_text,
                        "boost": 1
                    }
                }
            }],
            "filter": [{
                "exists": {
                    "field": "title-vector"
                }
            }]
        }
    }

    knn = {
        "field": "title-vector",
        "k": 1,
        "num_candidates": 20,
        "query_vector_builder": {
            "text_embedding": {
                "model_id": "sentence-transformers__all-distilroberta-v1",
                "model_text": query_text
            }
        },
        "boost": 24
    }

    fields = ["title", "body"]
    index = 'search-bank-transfers'
    resp = es.search(index=index,
                     query=query,
                     knn=knn,
                     fields=fields,
                     size=3,
                     source=False)

    body = resp['hits']['hits']

    return body


def truncate_text(text, max_tokens):
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text

    return ' '.join(tokens[:max_tokens])

# Generate a response from Gemini based on the given prompt
def generateResponse(prompt):
    response = model.generate_content(prompt, 
                                      generation_config=generation_config
    )
    return response.text

#image = Image.open('homecraft_logo.jpg')
st.image("https://i.imgur.com/G22hbgZ.png", caption=None)
st.title("Elastibank Search Bar")

# Main chat form
with st.form("chat_form"):
    query = st.text_input("You: ")
    submit_button = st.form_submit_button("Send")

# Generate and display response on form submission
negResponse = "I'm unable to answer the question based on the information I have from Homecraft dataset."
if submit_button:
    es = es_connect(cid, cu, cp)
    resp_docs = search_docs(query)
    prompt = f"Answer this question: {query}. Leverage the following docs to find the answer: {resp_docs}"
    answer = generateResponse(prompt)
    
    if negResponse in answer:
        st.write(f"Search Assistant: \n\n{answer.strip()}")
    else:
        st.write(f"Search Assistant: {answer.strip()}\n\n")

