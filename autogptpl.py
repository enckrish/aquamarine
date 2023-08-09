from transformers import AutoTokenizer, pipeline, logging, TextGenerationPipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import json

model_name_or_path = "TheBloke/WizardCoder-15B-1.0-GPTQ"
# Or to load it locally, pass the local download path
# model_name_or_path = "/path/to/models/TheBloke_WizardCoder-15B-1.0-GPTQ"

use_triton = False

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(model_name_or_path,
                                           use_safetensors=True,
                                           device="cuda:0",
                                           use_triton=use_triton,
                                           quantize_config=None)

# Prevent printing spurious transformers error when using pipeline with AutoGPTQ
logging.set_verbosity(logging.CRITICAL)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, return_full_text=False)

f = open('prompt_constants.json')
pc = json.load(f)
# prompt_template = (pc['templates'][0])


def analys(services: [str], prompt_template:str, pmt: str):
    print("H2")
    services = ", ".join(services)
    prompt = prompt_template.format(services=services, prompt=pmt)
    print(prompt)
    outputs = pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.1, top_k=50, top_p=0.95)
    return outputs[0]['generated_text']

# Prompt Template
# ---------------


# Prompt
# ------
# ~Logs straight away~
