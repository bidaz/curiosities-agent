import json
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_post():

    prompt = """
    Erstelle einen Instagram-Beitrag
    für die Seite:

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
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )
