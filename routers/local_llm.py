from fastapi import APIRouter, HTTPException
from models import AutoCompleteModel, ChatModel, ChatResponseModel
from transformers import pipeline, Pipeline
import logging
import torch

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# chat = APIRouter()  # Removed to avoid redefinition error

llm_local_router = APIRouter()


def generate_response(message: str) -> dict:
    # Use apenas a mensagem como prompt
    generator = pipeline("text-generation", model="gpt2")
    return generator(message)


# Initialize the text-generation pipeline once
try:
    logger.info("Loading text-generation pipeline...")
    generator: Pipeline = pipeline("text-generation", model="gpt2")
    logger.info("Pipeline loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load text-generation pipeline: {e}")
    generator = None


@llm_local_router.post("/autocomplete", response_model=ChatResponseModel, tags=["Local LLM"])
def autocomplete(body: AutoCompleteModel) -> ChatResponseModel:
    if not generator:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        response = generator(body.phrase, max_length=50, num_return_sequences=1)
        # Extract the generated text
        generated_text = response[0]["generated_text"]
        return ChatResponseModel(assistant=generated_text)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response.")

@llm_local_router.post("/chatcomplete", response_model=ChatResponseModel, tags=["Local LLM"])
async def chat(body: ChatModel) -> ChatResponseModel:
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.bfloat16,
    )
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot who always responds in the style of a pirate",
        },
        {"role": "user", "content": body.message},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True)
    
    prediction = pipe(
        prompt,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95)
    
    return ChatResponseModel(assistant=prediction[0]["generated_text"])