from transformers import AutoTokenizer, pipeline, logging, TextGenerationPipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import argparse

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

def analys(tmpl: str, pmt: str):
    prompt_template = tmpl
    prompt = prompt_template.format(prompt=pmt)

    outputs = pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.2, top_k=50, top_p=0.95)

    print(outputs[0])
    return outputs[0]['generated_text']

# Prompt Template
# ---------------
# You are given a block of logs from a running process. Identify the severity of the logs, which may be none, low, medium, high or critical. Also provide actionable insights, if the severity is not low, explain why you gave the severity in here. Also provide a review of the logs, from the viewpoint of a compliance monitoring service and software log analyzer.
# You should only give the response in JSON.
#
# SERVICE: services[].join(',') (like "Docker,PostgreSQL")
#
# ### LOGS:
# {prompt}
#
# ### RESPONSE:

# Prompt
# ------
# ~Logs straight away~

