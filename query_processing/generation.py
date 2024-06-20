from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import openai
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from model import llama_hf

# Prompt

    # template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for medical question-answering tasks about two rare diseases, Hypophosphatasia and Ehler-Danlos Syndrome. 
    # You have access to a database of medical documents ralated to the question they ask for context and only have the ability to answer questions based on the context provided.
    # Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
    # Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
    # Question: {question} 
    # Context: {context} 
    # Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",


prompt = PromptTemplate(

    template="""<|begin_of_text|><|start_header_id|>System<|end_header_id|> You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on 
    Hypophosphatasia and Ehlers-Danlos Syndrome. 
    You will be given relevant context to answer user queries. 
    Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
    Do not mention in your response that you were given context. Do not reference the context in your response at all.

    By looking at the above context, answer the following user question.

    <|eot_id|><|start_header_id|>user<|end_header_id|> 
    {question}
    {context}
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    
""",

    input_variables=["question", "context"],
)

llm = llama_hf


llama_generation = prompt | llm | StrOutputParser()

def generate(query, context):
    llama_response = llama_generation.invoke({"question": query, "context": context})

    openai_response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", 
            "content": """You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
            You will be given relevant context to answer user queries. 
            Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
            Do not mention in your response that you were given context. Do not reference the context in your response at all."""
        },
        {
            "role": "user", 
            "content": f'Question: {query} Context: {context}' 
        }
    ],
    temperature=0.3,
    max_tokens=700
)

    gpt_response = openai_response.choices[0].message.content

    if not gpt_response:
        gpt_response = "I'm sorry, but I couldn't generate a complete response. Could you please provide more details or try asking a more specific question?"


    return {gpt_response, llama_response}




