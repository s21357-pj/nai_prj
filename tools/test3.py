from haystack.pipelines import Pipeline
from haystack.nodes import Crawler, PreProcessor, ElasticsearchRetriever, FARMReader
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.document_stores import FAISSDocumentStore
from haystack.utils import fetch_archive_from_http
from haystack import Document
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import RAGenerator, DensePassageRetriever
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import print_answers
from haystack.utils import convert_files_to_docs, fetch_archive_from_http, clean_wiki_text

document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True)


retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="vblagoje/dpr-question_encoder-single-lfqa-wiki",
    passage_embedding_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki",
)

document_store.update_embeddings(retriever)

p_retrieval = DocumentSearchPipeline(retriever)
res = p_retrieval.run(query="Tell me something about Arya Stark?", params={"Retriever": {"top_k": 10}})
print_documents(res, max_text_len=512)