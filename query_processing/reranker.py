import torch
import chromadb
from query_processing.database_retrieval import embed_query, get_documents

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

    def rank_documents(self, query, documents):
        query_embeddings = embed_query(query)
        query_embeddings = torch.tensor([query_embeddings], dtype=torch.float32)

        scores = []
        for doc in documents['embeddings'][0]:
            doc_embeddings = torch.tensor(doc, dtype=torch.float32)  # Match data types
            score = self.max_sim(query_embeddings, doc_embeddings)
            scores.append(score.item())

        ranked_indices = torch.argsort(torch.tensor(scores), descending=True)
        # print(scores)   
        return [documents['documents'][0][i] for i in ranked_indices]
