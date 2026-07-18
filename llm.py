import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"


def ask_llm(prompt: str) -> str:
    if not GROQ_API_KEY:
        raise Exception(
            "GROQ_API_KEY is missing. Copy .env.example to .env and add your key."
        )

    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that writes clear, "
                               "professional, well-structured content.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        answer = response.choices[0].message.content
        return answer.strip()

    except Exception as error:
        raise Exception(f"Groq API call failed: {error}")