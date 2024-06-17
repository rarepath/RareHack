#Takes a query and returns chat response and a response code. End to end query processor.

from query_expansion import get_expanded_queries
from embedder import embed_query
from database_retrieval import get_documents
from reranker import rank_documents
from hallucination_grader import detect_hallucination

# Step 1: Query Expansion
# Step 2: Query Embedding
# Step 3: Document Retrieval
# Step 4: Re-ranking of documents
# Step 5: Hallucination Detection
# Step 6: Response Generation
# Step 7: Response Post-processing
# Step 8: Return response and response code


def process_query(query):
    # Step 1: Query Expansion
    expanded_queries = get_expanded_queries(query)
    
    # Step 2: Query Embedding
    query_embeddings = []
    for embedded_query in expanded_queries:
        query_embeddings.append(embed_query(embedded_query))
    
    # Step 3: Document Retrieval
    documents = []
    for query_embedding in query_embeddings:
        documents.append(get_documents(query_embedding))
    
    # Step 4: Re-ranking of documents
    ranked_documents = rank_documents(query, documents)
    
    # Step 5: Response Generation
    chatbot_response = generate_response(ranked_documents, query)

    # Step 6: Hallucination Detection
    is_hallucinating = detect_hallucinations(chatbot_response, query, ranked_documents)

    # Step 7: Response Post-processing
    api_response = post_process_response(chatbot_response)
    
    # Step 8: Return response and response code
    return chatbot_response, api_response
