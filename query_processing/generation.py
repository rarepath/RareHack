from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import openai
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from model import llama_hf

# Prompt

#  template="""System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
#     You will be given relevant context to answer user queries. 
#     Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
#     Do not mention in your response that you were given context. Do not reference the context in your response at all.

llama_prompt = PromptTemplate(
    template="""System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
You will be given relevant context to answer user queries. 
Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
Do not mention in your response that you were given context.

User: Question: {question} 
Context: {context}
Assistant:""",
    input_variables=["question", "context"],
)

llm = Ollama(model=llama_hf, temperature=0.2)


llama_generation = llama_prompt | llm | StrOutputParser()

def generate_llama(query, context):
    llama_response = llama_generation.invoke({"question": query, "context": context})

    return llama_response


def generate_gpt(query, context):
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


    return gpt_response




