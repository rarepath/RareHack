from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, QuantoConfig
import torch
from model_config import model_name
from langchain_huggingface import HuggingFacePipeline



quantization_config = QuantoConfig(weights="float8")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map = "auto", trust_remote_code=True, quantization_config=quantization_config)

prompt = """System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
    You will be given relevant context to answer user queries. 
    Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
    Do not mention in your response that you were given context. Do not reference the context in your response at all.
    {context}

    By looking at the above context, answer the following user question.

    User: {question}

    Assistant:<|eot_id|>
"""

question = "What other genes are associated or might be associated with TNXB variants that cause clEDS?"
tokenized_prompt = tokenizer(tokenizer.bos_token + prompt, return_tensors="pt").to(model.device)

outputs = model.generate(input_ids=tokenized_prompt.input_ids, attention_mask=tokenized_prompt.attention_mask, max_new_tokens=128, eos_token_id=terminators)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

response = outputs[0][tokenized_prompt.input_ids.shape[-1]:]
print(tokenizer.decode(response, skip_special_tokens=True))

