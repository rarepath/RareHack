import fitz  
import csv
import time
from query_expansion import get_expanded_queries, decorate_query
from database_retrieval import embed_query, get_documents
from reranker import MaxSimReranker
from hallucination_grader import check_hallucination
from generation import generate

def extract_questions_from_pdf(pdf_path):
    questions = []
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        current_question = ""
        for line in lines:
            line = ' '.join(line.split(' ')[1:]) if line[0].isdigit() else line
            if line.endswith('?'):
                current_question += " " + line
                questions.append(current_question.strip())
                current_question = ""
            else:
                current_question += " " + line
        if current_question:
            questions.append(current_question.strip())
    return questions

def process_query(query):
    start_time = time.time()  

    decorated_query = decorate_query(query)
    expanded_queries = get_expanded_queries(decorated_query)
    expanded_queries = [decorated_query] + expanded_queries

    query_embeddings = []
    for embedded_query in expanded_queries:
        query_embeddings.append(embed_query(embedded_query))
    
    retrieved_docs = get_documents(query_embeddings)

    ranked_documents = MaxSimReranker().rank_documents(decorated_query, retrieved_docs)

    top_documents = ranked_documents[:3]

    gpt_response, llama_response = generate(decorated_query, top_documents)

    check_hallucination(gpt_response, decorated_query, ranked_documents)
    check_hallucination(llama_response, decorated_query, ranked_documents)

    end_time = time.time()  
    response_time = end_time - start_time

    return gpt_response, llama_response, response_time

def process_and_save_responses(questions, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Question', 'Llama Response', 'GPT Response', 'Feedback', 'Response Time (seconds)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        total_response_time = 0
        for i, question in enumerate(questions):
            gpt_response, llama_response, response_time = process_query(question)
            total_response_time += response_time

            writer.writerow({
                'Question': question,
                'Llama Response': llama_response,
                'GPT Response': gpt_response,
                'Feedback': '',
                'Response Time (seconds)': response_time
            })

            # Print message after each question is processed
            print(f"Question {i+1} done in {response_time:.2f} seconds")

            # Calculate and print the updated average response time
            average_response_time = total_response_time / (i + 1)
            print(f"Updated average response time per question: {average_response_time:.2f} seconds")

pdf_path = 'List_Of_Questions.pdf'  
output_file = 'new_responses.csv'  
questions = extract_questions_from_pdf(pdf_path)

# Process all questions
process_and_save_responses(questions, output_file)
