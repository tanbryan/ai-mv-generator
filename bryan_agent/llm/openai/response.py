import openai
import requests
from typing import Any, Optional, Union
from PIL import Image
from io import BytesIO
from bryan_agent.utils.io import get_env
from bryan_agent.llm.openai.model import openai_models
from dotenv import load_dotenv
import json
from bryan_agent.utils.tool import parse_response_content

load_dotenv()

openai_api_key = get_env("OPENAI_API_KEY")
openai.api_key = openai_api_key

def get_openai_llm(
    model_name: Optional[str] = None,
    max_retries: Optional[int] = None,
    temperature: Optional[float] = None,
    **kwargs: Any,
):
    return {
        "llm_model_name": model_name,
        "openai_api_key": openai_api_key,
        "max_retries": max_retries or 3,
        "temperature": temperature or 0.5,
        **kwargs,
    }

def create_image_prompt(prompt: str, config: dict = None):
    config = config or get_openai_llm(model_name=openai_models["image_model"][0])
    response = openai.Image.create(
        model=config["llm_model_name"],
        prompt=prompt,
        size=config.get("size", "1024x1024"),
        quality=config.get("quality", "standard"),
        n=config.get("n", 1),
    )

    image_url = response['data'][0]['url']
    img_response = requests.get(image_url)

    if img_response.status_code == 200:
        img = Image.open(BytesIO(img_response.content))
        return img
    else:
        print(f"Failed to view image from URL: {image_url}")
        return None

def create_chat_completion(messages: list, config: dict = None, parse_response: bool = True):
    config = config or get_openai_llm(model_name=openai_models["text_model"][0])
    max_retries = config.get("max_retries", 3)
    
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=config["llm_model_name"],
                messages=messages,
                temperature=config["temperature"],
                max_tokens=config.get("max_tokens", 4096),
                top_p=config.get("top_p", 1.0),
                frequency_penalty=config.get("frequency_penalty", 0.0),
                presence_penalty=config.get("presence_penalty", 0.0),
            )
            
            content = response['choices'][0]['message']['content']

            if parse_response:
                return parse_response_content(content)
            else:
                return content
        except (openai.error.InvalidRequestError, json.JSONDecodeError, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise