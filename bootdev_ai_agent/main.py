import os
from dotenv import load_dotenv
from google import genai 
import sys
from google.genai import types
import argparse
from config import *
from call_function import available_functions, call_function

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="An AI agent CLI tool.")
    parser.add_argument("prompt", type=str, help="The user's prompt for the AI agent.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    user_prompt = args.prompt
    is_verbose = args.verbose

    if len(sys.argv) == 1:
        print("error: no prompt given")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if is_verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    generate_content(client, messages, is_verbose)

def generate_content(client, messages, is_verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        return response.text 
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, is_verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if is_verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")



if __name__ == "__main__":
    main()
