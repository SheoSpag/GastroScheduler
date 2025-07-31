import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY2")
)

MODEL = "google/gemini-2.5-pro-exp-03-25"

def generate_shifts(prompt: str):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Sos un planificador de turnos. Respondé únicamente con JSON válido, sin explicaciones."},
            {"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
