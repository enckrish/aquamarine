from jsonformer import Jsonformer
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.cuda import is_available

is_available()

repo_ids = ['togethercomputer/LLaMA-2-7B-32K', 'PygmalionAI/pygmalion-6b', 'microsoft/DialoGPT-medium']

model = AutoModelForCausalLM.from_pretrained(repo_ids[2])
tokenizer = AutoTokenizer.from_pretrained(repo_ids[2])

json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
        "is_student": {"type": "boolean"},
        "courses": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

prompt = "Generate a person's information based on the following schema:"
jsonformer = Jsonformer(model, tokenizer, json_schema, prompt)
generated_data = jsonformer()

print(generated_data)