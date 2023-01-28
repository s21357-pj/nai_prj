import logging

import pandas as pd
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from haystack.utils import fetch_archive_from_http
from haystack import Document
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import RAGenerator, DensePassageRetriever
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import print_answers
from haystack.nodes import TransformersSummarizer
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import spacy
from googletrans import Translator

translator = Translator()


@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)


app = FastAPI()
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe("language_detector")


class Item(BaseModel):
    question: str


# Download sample
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s",
                    level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

document_store = FAISSDocumentStore.load(index_path="docs.index")

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


pipe = GenerativeQAPipeline(generator=generator, retriever=retriever)


@app.post("/api/ask")
def update_item(item: Item):
    q = nlp(item.question)
    detect_language = q._.language
    res = pipe.run(query=translator.translate(item.question, dest='en').
                   text, params={"Generator": {"top_k": 1},
                                 "Retriever": {"top_k": 1}})
    if detect_language["language"] == 'en':
        ans = res["answers"][0].answer
    else:
        ans = translator.translate(res["answers"][0].answer, dest='pl').text
    return {"ans": ans}

