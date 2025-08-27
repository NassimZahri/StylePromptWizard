import os
import base64
from groq import Groq
from dotenv import load_dotenv
import requests
from pathlib import Path

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def generate_image_prompt(image_path_or_url, question):
    """
    Generate an image prompt using Groq API.

    Args:
        image_path_or_url: Local path to an image file or URL to an image
        question: The prompt/question to ask about the image

    Returns:
        Generated prompt as a string
    """
    try:
        # Determine if input is a URL or local file
        if image_path_or_url.startswith(("http://", "https://")):
            # It's a URL
            image_url = image_path_or_url
        else:
            # It's a local file path - read and encode the image to base64
            image_path = Path(image_path_or_url).resolve()
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # For local files, upload to a public image hosting service or use a data URI
            # Here we're using a temporary public URL for testing purposes
            # In production, you should use proper image hosting or cloud storage

            # For now, let's use data URI with base64 encoding
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            # Create a data URI for the image
            file_extension = image_path.suffix[1:].lower()
            image_url = f"data:image/{file_extension};base64,{encoded_image}"

        # Generate the prompt using Groq's LLM
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing images and generating detailed, accurate prompts for image generation tools. Focus on visual elements, style, composition, lighting, and mood. Your response should only contain the prompt text with no additional commentary.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                },
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=500,
            temperature=0.2,  # Lower temperature for more consistent outputs
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Error generating image prompt: {str(e)}")
