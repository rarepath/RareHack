import torch
import chromadb
from database_retrieval import embed_query, get_documents

class MaxSimReranker:
    def __init__(self):
        pass

    def max_sim(self, query_embeddings, doc_embeddings):
        max_similarities = []
        for query_token in query_embeddings:

            query_token = query_token.unsqueeze(1) if query_token.dim() == 1 else query_token

            similarities = torch.matmul(doc_embeddings, query_token)
            max_similarity = torch.max(similarities)
            max_similarities.append(max_similarity)
        return torch.sum(torch.stack(max_similarities))

    def rank_documents(self, query_embeddings, documents):
        scores = []
        for doc in documents['embeddings'][0]:
            print(len(doc))
            doc_embeddings = torch.tensor(doc, dtype=torch.float32)  # Match data types
            print(doc_embeddings.shape )
            score = self.max_sim(query_embeddings, doc_embeddings)
            scores.append(score.item())

        ranked_indices = torch.argsort(torch.tensor(scores), descending=True)
        print(ranked_indices)   
        return [documents['documents'][0][i] for i in ranked_indices]

# Initialize the reranker
# reranker = MaxSimReranker()

# # Example query
# query = "What is hypophosphatasia?"
# query_embedding = embed_query(query)
# query_embeddings = torch.tensor([query_embedding], dtype=torch.float32)
# # Retrieve documents and their embeddings
# documents = get_documents(query_embedding)
# # print(documents)
# # Re-rank documents
# reranked_documents = reranker.rank_documents(query_embeddings, documents)
# print(reranked_documents)




# query_embeddings = torch.tensor([[0.1, 0.2, 0.3]], dtype=torch.float32)
# documents = [{
#     'embedding': [0.1, 0.2, 0.3],
#     'metadata': {'text': 'Document 1'}
# }, {
#     'embedding': [0.4, 0.5, 0.6],
#     'metadata': {'text': 'Document 2'}
# }]

# for doc in documents:
#     doc['embedding'] = torch.tensor(doc['embedding'], dtype=torch.float32).unsqueeze(0)

# reranked_documents = reranker.rank_documents(query_embeddings, documents)



# # Display only the re-ranked document texts
# for doc, score in reranked_documents:
#     print(doc)