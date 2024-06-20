from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from model_config import model_name
from langchain_huggingface import HuggingFacePipeline



    

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map = "auto", trust_remote_code=True)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens = 1000)
llama_hf = HuggingFacePipeline(pipeline=pipe)





