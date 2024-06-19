from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain import LanguageModel
import torch
from torch.quantization import quantize_dynamic
from model_config import model_name, model_quantization, model_size


    
'''quantize_dynamic(
        model,  # the original model
        {torch.nn.Linear},  # a set of layers to quantize
        dtype=torch.qint8  # the target data type
    )    
'''

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)



print(llama_model.generate("What are the symptoms of hypophosphatasia?"))



