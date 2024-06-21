#Takes a query and returns chat response and a response code. End to end query processor.

from query_processing.query_expansion import get_expanded_queries, decorate_query
from query_processing.database_retrieval import embed_query
from query_processing.database_retrieval import get_documents
from query_processing.reranker import MaxSimReranker
from query_processing.hallucination_grader import check_hallucination
from query_processing.generation import generate_gpt, generate_llama
from query_processing.summarizer import summarize

def process_query(query, summary=''):
    # Step 1: Query Expansion
    decorated_query = decorate_query(query)
    expanded_queries = get_expanded_queries(decorated_query)
    expanded_queries = [decorated_query] + expanded_queries
    # print(expanded_queries)
    
    # Step 2: Query Embedding
    query_embeddings = []
    for embedded_query in expanded_queries:
        query_embeddings.append(embed_query(embedded_query))
    
    # Step 3: Document Retrieval
    retrieved_docs = get_documents(query_embeddings)

        
    # Step 4: Re-ranking of documents
    ranked_documents = MaxSimReranker().rank_documents(decorated_query, retrieved_docs)
    # print(ranked_documents)
    # Step 5: Response Generation
    gpt_response = generate_gpt(decorated_query, ranked_documents[:3])
    llama_response = generate_llama(decorated_query, ranked_documents[:3])


    # # Step 6: Hallucination Detection
    is_hallucinating_llama = check_hallucination(llama_response, decorated_query, ranked_documents[:3])
    is_hallucinating_gpt = check_hallucination(gpt_response, decorated_query, ranked_documents[:3])

    # print("llama:", is_hallucinating_llama) 
    # print("gpt:", is_hallucinating_gpt) 
    # # Step 7: Response Post-processing
    summary = summarize(decorated_query, gpt_response)
    # # Step 8: Return response and response code
    return [gpt_response, llama_response, summary]



# Example usage
# query = "What is HPP?"
# gpt_response, llama_response, summary = process_query(query)
# print("GPT Response:", gpt_response)
# print("LLAMA Response:", llama_response)
# print("Summary:", summary)