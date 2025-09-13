import os
from dotenv import load_dotenv
from google import genai 
import sys
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) == 1:
    print("error: no prompt given")
    sys.exit(1)
messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

parser = argparse.ArgumentParser(description="An AI agent CLI tool.")
parser.add_argument("prompt", type=str, help="The user's prompt for the AI agent.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
args = parser.parse_args()

user_prompt = args.prompt
is_verbose = args.verbose

print(response.text)
if is_verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
