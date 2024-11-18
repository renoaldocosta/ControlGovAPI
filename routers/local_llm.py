from fastapi import APIRouter, HTTPException
from models import AutoCompleteModel, ChatModel, ChatResponseModel, ChatResponseModelWithInformations
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


@llm_local_router.post("/autocomplete", response_model=ChatResponseModel, tags=["Local LLM"], description="Instruct the model to generate a response based on the input message using GPT-2")
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

# =============      Local LLM TinyLlama-1.1B-Chat-v1.0 ======================
@llm_local_router.post("/chatcomplete_1", response_model=ChatResponseModel, tags=["Local LLM"], description="Instruct the model to generate a response based on the input message using TinyLlama-1.1B-Chat-v1.0")
async def chat_1(body: ChatModel) -> ChatResponseModel:
    try:
        pipe = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            torch_dtype=torch.bfloat16,
        )
    except Exception as e:
        logging.error(f"Failed to load text-generation pipeline: {e}")
        raise HTTPException(status_code=500, detail="Model is not loaded.")
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
    try:
        prediction = pipe(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95)
        
        return ChatResponseModel(assistant=prediction[0]["generated_text"])
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        raise HTTPException(status_code=503, detail="Failed to generate response.")

    
# =============      Local LLM HuggingFaceTB/SmolLM2-135M-Instruct ======================
@llm_local_router.post("/chatcomplete_2", response_model=ChatResponseModelWithInformations, tags=["Local LLM"], description="Instruct the model to generate a response based on the input message using HuggingFaceTB/SmolLM2-135M-Instruct")
async def chat_2(body: ChatModel) -> ChatResponseModelWithInformations:
    pipe = pipeline(
        "text-generation",
        model="HuggingFaceTB/SmolLM2-360M-Instruct",
        torch_dtype=torch.bfloat16,
    )
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot who always responds in a formal about the value for the code.",
        },
        {"role": "user", "content": f"From this text: '{body.message}'. What is the value?"},
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
    
    return ChatResponseModelWithInformations(processed_text=body.message,task_type="text-generation" , assistant=prediction[0]["generated_text"].split('<|im_start|>assistant\n')[-1])