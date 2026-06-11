import json
import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post():
    prompt = """
    Erstelle einen Instagram-Beitrag für die Seite:
    Kurioses aus aller Welt

    Antworte ausschließlich als JSON:

    {
      "topic":"",
      "title":"",
      "body":"",
      "hashtags":"",
      "image_prompt":""
    }
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)


def generate_image_file(image_prompt, filename):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(filename, "wb") as f:
        f.write(image_bytes)

    return filename
