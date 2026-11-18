
import json
import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()
PROMPT = "Explain token usage in exactly one short sentence."

def show_result(name, model, reply, input_tokens, output_tokens, input_price, output_price):

    cost = (input_tokens * input_price + output_tokens * output_price) / 1_000_000

    print(f"\n--- {name} ---")
    print(f"Reply: {reply}")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Estimated paid-tier cost: ${cost:.8f}")
    print("(Actual charge may be $0 on the free tier)")

    return {
        "provider": name.lower(),
        "model": model,
        "reply": reply,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_price_per_m": input_price,
        "output_price_per_m": output_price,
        "cost_usd": cost
    }


def main():

    if not os.getenv("GEMINI_API_KEY") or not os.getenv("GROQ_API_KEY"):
        print("Error: Missing API keys. Please check your .env file.")
        return

    gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    g = gemini.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=PROMPT
    )

    gemini_result = show_result(
        "gemini", "gemini-3.5-flash-lite", g.text,
        g.usage_metadata.prompt_token_count,
        g.usage_metadata.candidates_token_count,
        0.30, 2.50
    )

    groq = Groq(api_key=os.environ["GROQ_API_KEY"])
    r = groq.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": PROMPT}]
    )

    groq_result = show_result(
        "groq", "openai/gpt-oss-20b", r.choices[0].message.content,
        r.usage.prompt_tokens,
        r.usage.completion_tokens,
        0.075, 0.30
    )

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(
            [gemini_result, groq_result],
            f,
            indent=2
        )

    print("\nResults saved to results.json")


if __name__ == "__main__":
    main()
