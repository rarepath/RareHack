#Takes a query and returns chat response and a response code. End to end query processor.

from query_expansion import get_expanded_queries, decorate_query
from database_retrieval import embed_query
from database_retrieval import get_documents
from reranker import MaxSimReranker
from hallucination_grader import check_hallucination
from generation import generate



def process_query(query):
    # Step 1: Query Expansion
    decorated_query = decorate_query(query)
    expanded_queries = get_expanded_queries(decorated_query)
    expanded_queries = [decorated_query] + expanded_queries
    print(expanded_queries)
    
    # Step 2: Query Embedding
    query_embeddings = []
    for embedded_query in expanded_queries:
        query_embeddings.append(embed_query(embedded_query))
    
    # Step 3: Document Retrieval
    retrieved_docs = get_documents(query_embeddings)


    #unpack documents
        
    # Step 4: Re-ranking of documents
    ranked_documents = MaxSimReranker().rank_documents(decorated_query, retrieved_docs)
    # print(ranked_documents)
    # Step 5: Response Generation
    gpt_response, llama_response = generate(decorated_query, ranked_documents[:3])


    # # Step 6: Hallucination Detection
    is_hallucinating_llama = check_hallucination(llama_response, decorated_query, ranked_documents)
    is_hallucinating_gpt = check_hallucination(gpt_response, decorated_query, ranked_documents)

    print("llama:", is_hallucinating_llama) 
    print("gpt:", is_hallucinating_gpt) 
    # # Step 7: Response Post-processing
    # api_response = post_process_response(chatbot_response)
    
    # # Step 8: Return response and response code
    return [gpt_response, llama_response]



# Example usage
query = "What other genes are associated or might be associated with TNXB variants that cause clEDS?"
for resp in process_query(query):
    print(resp, end ="\n\n\n\n")