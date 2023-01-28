import logging

import pandas as pd
import json
from haystack.utils import fetch_archive_from_http
from haystack import Document
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import RAGenerator, DensePassageRetriever
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import print_answers
from pathlib import Path

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

documents = []
# assign directory
directory = 'crawled_files'

# iterate over files in
# that directory
files = Path(directory).glob('*')
for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        title = data["meta"]["url"].replace("https://en.m.wikipedia.org/wiki/", "")
        documents.append(Document(content=data["content"],
                                  meta={"name": title or ""}))

document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True)

# Initialize DPR Retriever to encode documents, encode question and query documents
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    use_gpu=True,
    embed_title=True,
)

# Initialize RAG Generator
generator = RAGenerator(
    model_name_or_path="facebook/rag-token-nq",
    use_gpu=True,
    top_k=1,
    max_length=200,
    min_length=2,
    embed_title=True,
    num_beams=2,
)



# Delete existing documents in documents store
document_store.delete_documents()

# Write documents to document store
document_store.write_documents(documents)

# Add documents embeddings to index
document_store.update_embeddings(retriever=retriever)

QUESTIONS = [
    "definition of network"
]


pipe = GenerativeQAPipeline(generator=generator, retriever=retriever)
for question in QUESTIONS:
    res = pipe.run(query=question, params={"Generator": {"top_k": 1}, "Retriever": {"top_k": 5}})
    print_answers(res, details="minimum")