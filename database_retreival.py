import chromadb
import openai
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
print(chroma_client.list_collections())


def embed_query(query):
    pass
   

def get_documents():
    pass

