from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
openai = OpenAI(
    api_key=os.getenv('DEEPINFRA_API_KEY'),
    base_url="https://api.deepinfra.com/v1/openai",
)

# Function to convert image to base64
def image_to_base64(image_path, size=(300, 300)):
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue())
    return encoded_string.decode('utf-8')

# Function to query the bot with either text or multimodal input
def query_bot(messages, prompt, image_path=None):
    # If an image is provided, process the image and create a multimodal prompt
    if image_path:
        image_base64 = image_to_base64(image_path)
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
            ]
        })
    else:
        # Regular text-based prompt
        messages.append({"role": "user", "content": prompt})

    # Send the query to the API
    chat_completion = openai.chat.completions.create(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        messages=messages,
    )

    # Append the assistant's response to the conversation
    messages.append({
        "role": "assistant",
        "content": chat_completion.choices[0].message.content
    })
    
    return messages

# Example usage
# Regular text prompt
# messages = query_bot([], "What is the capital of France?")

# Multimodal prompt with image
# messages = query_bot([], "What can you tell me about this image?", image_path="/home/shujaat/Downloads/images.png")
# print(messages[-1])
