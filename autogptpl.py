import collections
from typing_extensions import Unpack
from typing import TypedDict, List
import logging
import json

from transformers import AutoTokenizer, pipeline, logging as TfLogging, TextGenerationPipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig


model_name_or_path = "TheBloke/WizardCoder-15B-1.0-GPTQ"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
model = AutoGPTQForCausalLM.from_quantized(model_name_or_path,
                                           use_safetensors=True,
                                           device="cuda:0",
                                           use_triton=False,
                                           quantize_config=None)

# Prevent printing spurious transformers error when using pipeline with AutoGPTQ
TfLogging.set_verbosity(logging.CRITICAL)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, return_full_text=False)

# f = open('prompt_constants.json')
# pc = json.load(f)
# prompt_template = (pc['templates'][0])

logger = logging.getLogger()


class PromptTemplateParams(TypedDict):
    service: str
    history: List[str]
    recent: List[str]


def to_numbered_paragraph(logs: List[str], label, sep=' '):
    return "\n".join(
        [f"{label} {i+1}:{sep}{e}" for i, e in enumerate(logs)]
    ).strip()


history_template = "####LOGS:\n{recent}\n####RESPONSE:\n{generated}\n"


# TODO in the seperated version, prompt_template arg will be removed,
# each analyzer will have a given prompt template
def analyze_log(prompt_template: str, **kwargs: Unpack[PromptTemplateParams]):
    kwargs["history"] = to_numbered_paragraph(kwargs["history"], label="Entry", sep='\n')
    kwargs["recent"] = to_numbered_paragraph(kwargs["recent"], label="Line")
    prompt = prompt_template.format(**kwargs)

    outputs = pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.1, top_k=50, top_p=0.95)

    gen_text = outputs[0]['generated_text']
    print(gen_text)

    history_item = history_template.format(recent=kwargs["recent"], generated=gen_text)
    return convert_llm_o_to_json(gen_text), history_item


severity_map = collections.defaultdict(int)
# Rating: 0 is reserved for invalid LLM response
severity_map["none"] = 1
severity_map["low"] = 2
severity_map["medium"] = 3
severity_map["high"] = 4
severity_map["critical"] = 5


def convert_llm_o_to_json(out: str):
    # Returns formatted/verified output as current analysis
    fmt_out = {"rating": 0, "actionable_insights": [], "review": "", "citation": 0}

    if len(out) <= 7 or out[:7] != '```json' or out[-3:] != '```':
        logger.warning("JSON-Conv failed")
        fmt_out["review"] = "JSON-Conv failed, raw output: {}".format(out)
        return fmt_out

    out_json = out[7:-3]
    try:
        out_json = json.loads(out_json)
    except json.JSONDecodeError as e:
        logger.warning("JSON-Conv failed")
        fmt_out["review"] = "JSON-Conv failed, raw output: {}".format(out_json)
        return fmt_out

    fmt_out['rating'] = severity_map[str(out_json['rating']).lower()]
    fmt_out['actionable_insights'] = out_json['actionable_insights']
    fmt_out['review'] = out_json['review']
    fmt_out['citation'] = out_json['citation']

    return fmt_out
