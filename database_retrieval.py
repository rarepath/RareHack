import chromadb
import openai
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
print(chroma_client.list_collections())



def embed_query(query):
    # Embed the query using OpenAI's API
    response = openai.Embed.create(model="text-davinci-003", objects=[{"object": "text", "text": query}])
    return response['embedding']


   

def get_documents(query_embedding):
    collection = chroma_client.get_collection('section-embeddings')
    # Get the documents from the database
    documents = collection.query(query_embedding, k=5, include=["metadata"])
    return documents


