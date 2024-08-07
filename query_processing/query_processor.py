#Takes a query and returns chat response and a response code. End to end query processor.

from query_processing.query_expansion import get_expanded_queries, decorate_query
from query_processing.database_retrieval import embed_query, get_documents
from query_processing.reranker import MaxSimReranker
from query_processing.generation import generate_gpt, generate_llama

from query_processing.summarizer import summarize

hallucination_response = "I'm sorry, I don't have enough information to answer that question."
def process_query(query, model_selection, summary=''):
    # Step 1: Query Expansion
    decorated_query = decorate_query(query)
    expanded_queries = get_expanded_queries(decorated_query)
    expanded_queries = [decorated_query] + expanded_queries
    print("Expanding Queries")
    
    # Step 2: Query Embedding
    query_embeddings = []
    for embedded_query in expanded_queries:
        query_embeddings.append(embed_query(embedded_query))
    print("Embedding Queries")
    
    # Step 3: Document Retrieval
    retrieved_docs = get_documents(query_embeddings)
    print("Retrieving Documents")

        
    # Step 4: Re-ranking of documents
    ranked_documents = MaxSimReranker().rank_documents(decorated_query, retrieved_docs)
    print("Re-ranking Documents")
    # Step 5: Response Generation
    try:
        urls = [doc[1]['URL'] for doc in ranked_documents[:3]]
    except:
        urls = []
    if model_selection == "gpt":
        gpt_response = generate_gpt(decorated_query, ranked_documents[:3], summary)
        print("Generating GPT Response")

        summary = summarize(decorated_query, gpt_response)
        return [gpt_response, urls, decorated_query + summary]

    elif model_selection == "llama":
        llama_response = generate_llama(decorated_query, ranked_documents[:3], summary)
        print("Generating LLAMA Response")

        summary = summarize(decorated_query, llama_response)
        return [llama_response, urls, decorated_query + summary]
    
    else:
        gpt_response = generate_gpt(decorated_query, ranked_documents[:3], summary)
        print("Generating GPT Response")

        llama_response = generate_llama(decorated_query, ranked_documents[:3], summary)
        print("Generating LLAMA Response")

        summary = summarize(decorated_query, llama_response)
        return [gpt_response, llama_response, urls, decorated_query + summary]





# Example usage
# query = "What is HPP?"
# gpt_response, llama_response, summary = process_query(query)
# print("GPT Response:", gpt_response)
# print("LLAMA Response:", llama_response)
# print("Summary:", summary)