from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import openai
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, QuantoConfig
import torch
from model_config import model_name
from langchain_huggingface import HuggingFacePipeline


quantization_config = QuantoConfig(weights="float8")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
                                             model_name, 
                                             pad_token_id=tokenizer.eos_token_id,
                                             device_map = "auto", 
                                             trust_remote_code=True, 
                                             quantization_config=quantization_config
                                             )


# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens = 1000)
# llama_hf = HuggingFacePipeline(pipeline=pipe)




def get_formatted_input(messages, context):
    system = """System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
        You will be given relevant context to answer user queries. 
        Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
        Do not mention in your response that you were given context."""
    instruction = "Please give a full and complete answer for the question."

    for item in messages:
        if item['role'] == "user":
            ## only apply this instruction for the first user turn
            item['content'] = instruction + " " + item['content']
            break

    conversation = '\n\n'.join(["User: " + item["content"] if item["role"] == "user" else "Assistant: " + item["content"] for item in messages]) + "\n\nAssistant:"
    formatted_input = system + "\n\n" + str(context) + "\n\n" + conversation
    
    return formatted_input




def generate_llama(query, context):
    # llama_prompt = PromptTemplate(
    #     template="""System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
    #     You will be given relevant context to answer user queries. 
    #     Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
    #     Do not mention in your response that you were given context.
        
    #     User: Question: {question} 
    #     Context: {context}
    #     Assistant:""",
    # input_variables=["question", "context"],
    # )

    messages = [
    {"role": "user", "content": f"{query}"}
    ]

    formatted_input = get_formatted_input(messages, context)
    tokenized_prompt = tokenizer(tokenizer.bos_token + formatted_input, return_tensors="pt").to(model.device)
    terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

    outputs = model.generate(input_ids=tokenized_prompt.input_ids, attention_mask=tokenized_prompt.attention_mask, max_new_tokens=128, eos_token_id=terminators)

    response = outputs[0][tokenized_prompt.input_ids.shape[-1]:]
    return tokenizer.decode(response, skip_special_tokens=True)



    # llama_generation = llama_prompt | llama_hf | StrOutputParser()


    # llama_response = llama_generation.invoke({"question": query, "context": context})



    return llama_response


def generate_gpt(query, context):
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




