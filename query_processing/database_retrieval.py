import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
# print(chroma_client.list_collections())



def embed_query(query): 
    # Embed the query using OpenAI's API
    response = OpenAI().embeddings.create(input = [query], model='text-embedding-3-large').data[0]
    # response = model.encode(query) 
    # response = chroma_client.get_embedding('text-embedding-3-large', query)
    return response.tolist()

   

def get_documents(queries_embeddings):
    collection = chroma_client.get_collection('vector-store-rare-diseases1')
    # Get the documents from the database
    documents = collection.query(
                                    query_embeddings=queries_embeddings, 
                                    n_results=9, 
                                    include=["documents", "embeddings"])
                                    # include=["metadatas", "embeddings", "documents"])
    
    return documents



#example usage
# query = ["What is Hypophosphatasia?", "What are the symptoms of Hypophosphatasia?"]
# query_embedding = embed_query(query)
# documents = get_documents(query_embedding) 
# print(documents)