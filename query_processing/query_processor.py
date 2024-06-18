#Takes a query and returns chat response and a response code. End to end query processor.

from query_expansion import get_expanded_queries
from database_retrieval import embed_query
from database_retrieval import get_documents
from reranker import MaxSimReranker
from hallucination_grader import check_hallucination

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
    print(expanded_queries)
    
    # Step 2: Query Embedding
    query_embeddings = []
    for embedded_query in expanded_queries:
        query_embeddings.append(embed_query(embedded_query))
    
    # Step 3: Document Retrieval
    documents_text = []
    documents_embeddings = []
    documents_metadata = []

    for query_embedding in query_embeddings: 
        #TODO
        gd_dict = get_documents(query_embedding)
        documents_text.append(gd_dict['documents'])
        documents_embeddings.append(gd_dict['embeddings'][0])
        documents_metadata.append(gd_dict['metadata']) 
        '''
        All we care about is the text, embeddings and metadata of the documents.

        
        
        
        '''

    #unpack documents
        
    # Step 4: Re-ranking of documents
    ranked_documents = MaxSimReranker().rank_documents(query, documents)
    print(ranked_documents)
    # # Step 5: Response Generation
    # chatbot_response = generate(query, ranked_documents)

    # # Step 6: Hallucination Detection
    # is_hallucinating = detect_hallucinations(chatbot_response, query, ranked_documents)

    # # Step 7: Response Post-processing
    # api_response = post_process_response(chatbot_response)
    
    # # Step 8: Return response and response code
    return documents



# Example usage
query = "What are the symptoms of hypophosphatasia?"
print( process_query(query))