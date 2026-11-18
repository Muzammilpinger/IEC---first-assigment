import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()
PROMPT = "Explain token usage in exactly one short sentence."

def show_result(name, reply, input_tokens, output_tokens, input_price, output_price):

    cost = (input_tokens * input_price + output_tokens * output_price) / 1_000_000

    print(f"\n--- {name} ---")
    print(f"Reply: {reply}")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Estimated paid-tier cost: ${cost:.8f}")
    print("(Actual charge may be $0 on the free tier)")


def main():
    gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    g = gemini.models.generate_content(         
        model="gemini-3.5-flash-lite",       ## THESE LINES WERE WRITTEN BY AI. 
        contents=PROMPT                      ## THO I UNDERSTAND EVERYTHING
    )

    show_result(
        "Gemini", g.text,
        g.usage_metadata.prompt_token_count,
        g.usage_metadata.candidates_token_count,
        0.10, 0.40
    )

    groq = Groq(api_key=os.environ["GROQ_API_KEY"])
    r = groq.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": PROMPT}]
    )
    show_result(
        "Groq", r.choices[0].message.content,
        r.usage.prompt_tokens,
        r.usage.completion_tokens,
        0.075, 0.30
    )

if __name__ == "__main__":
    main()