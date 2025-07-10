import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(dotenv_path="GEMINI_API_KEY.env")
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    args = sys.argv[1:]
    verbose = False

    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    user_prompt = ' '.join(args)

    
    
    #prompt = ' '.join(sys.argv[1:])

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
    )

    print(response.text)

    if verbose:
        print(f'User prompt: "{user_prompt}"')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
