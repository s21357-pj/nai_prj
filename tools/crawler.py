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

document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True)

crawler = Crawler(
    urls=["https://en.m.wikipedia.org/wiki/Computer_network",
          "https://en.m.wikipedia.org/wiki/Internet",
          "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users",
          "https://en.wikipedia.org/wiki/RIPE",
          "https://en.m.wikipedia.org/wiki/Routing",
          "https://en.wikipedia.org/wiki/Router_(computing)",
          "https://en.wikipedia.org/wiki/Server_(computing)",
          ],   # Websites to crawl
    crawler_depth=1,    # How many links to follow
    output_dir="crawled_files",  # The directory to store the crawled files, not very important, we don't use the files in this example
    filter_urls= ["https:\/\/en\.m\.wikipedia\.org\/wiki\/.*", "https:\/\/fcit\.usf\.edu\/network\/.*", "http://www.rfc-editor.org/rfc/.*\.txt"],
)
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
    split_by="word",
    split_length=500,
    split_respect_sentence_boundary=True,
)
indexing_pipeline = Pipeline()
indexing_pipeline.add_node(component=crawler, name="crawler", inputs=['File'])
indexing_pipeline.add_node(component=preprocessor, name="preprocessor", inputs=['crawler'])
indexing_pipeline.add_node(component=document_store, name="document_store", inputs=['preprocessor'])

indexing_pipeline.run(params={"crawler": {'return_documents': True}})


#
# Step 2: Use the data to answer questions.
#

# NOTE: You can run this code as many times as you like.

# Let's create a query pipeline. It will contain:
#  1. A Retriever that gets the relevant documents from the document store.
#  2. A Reader that locates the answers inside the documents.
#retriever = DensePassageRetriever(
#    document_store=document_store,
#    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
#    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
#    use_gpu=True,
#    embed_title=True,
#)
#
## Initialize RAG Generator
#generator = RAGenerator(
#    model_name_or_path="facebook/rag-token-nq",
#    use_gpu=True,
#    top_k=1,
#    max_length=200,
#    min_length=2,
#    embed_title=True,
#    num_beams=2,
#)
#
#
#document_store.update_embeddings(retriever=retriever)
#document_store.save(index_path="docs.index")
#
#QUESTIONS = [
#    "definition of computer network"
#]
#
#pipe = GenerativeQAPipeline(generator=generator, retriever=retriever)
#for question in QUESTIONS:
#    res = pipe.run(query=question, params={"Generator": {"top_k": 1}, "Retriever": {"top_k": 5}})
#    print_answers(res, details="medium")
