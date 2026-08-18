import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_PATH = Path(__file__).resolve().parent.parent.parent.parent / "model" / "trained_adapter" / "lora_adapter_v2"

print("Loading base model... (this happens once, may take a minute)")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32)
model = PeftModel.from_pretrained(base_model, str(ADAPTER_PATH))
model.eval()
print("Model with fine-tuned adapter loaded successfully.")

ALPACA_PROMPT = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""


def generate_response(instruction: str, input_text: str, max_new_tokens: int = 200) -> str:
    prompt = ALPACA_PROMPT.format(instruction, input_text, "")
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )

    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_text.split("### Response:")[-1].strip()
    return response