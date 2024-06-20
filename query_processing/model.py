from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, QuantoConfig
import torch
from model_config import model_name
from langchain_huggingface import HuggingFacePipeline



quantization_config = QuantoConfig(weights="float8")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map = "auto", trust_remote_code=True, quantization_config=quantization_config)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens = 1000, temperature=0.2)
llama_hf = HuggingFacePipeline(pipeline=pipe)





