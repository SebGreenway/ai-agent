import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.system_prompt import system_prompt
from functions.get_files_info import available_functions
from functions.call_function import call_function

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

    combined_prompt = f"{system_prompt}\n\nUser input: {user_prompt}"

    messages = [
        types.Content(role="user", parts=[types.Part(text=combined_prompt)]),
    ]

    max_iterations = 20

    for iteration in range(max_iterations):
        if verbose:
            print(f"\n--- ITERATION {iteration + 1} ---")

        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error during LLM call: {e}")
            break

        # Add all candidates' content to messages to keep conversation context
        for candidate in response.candidates:
            messages.append(candidate.content)

        # If there's a function call, handle it
        if response.candidates and response.candidates[0].content.parts[0].function_call:
            function_call_part = response.candidates[0].content.parts[0].function_call

            if verbose:
                print(f"Function call detected: {function_call_part.name}({function_call_part.args})")

            function_call_result = call_function(function_call_part, verbose=verbose)

            if not function_call_result.parts or not function_call_result.parts[0].function_response or not function_call_result.parts[0].function_response.response:
                raise Exception("Fatal: Function call returned no valid function_response!")

            messages.append(function_call_result)

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            continue  # proceed to next iteration

        else:
            # Plain text response — might be final or might be a plan
            final_text = response.text.strip()
            print(final_text)

            # Check for common phrases indicating completion
            done_phrases = [
                "I have fixed",
                "Bug fixed",
                "The bug is fixed",
                "Fixed the bug",
                "I fixed the bug",
            ]

            if any(phrase in final_text for phrase in done_phrases):
                break  # done

            else:
                # Not done yet — add as model message and continue
                messages.append(types.Content(role="model", parts=[types.Part(text=final_text)]))
                continue

    else:
        print("Reached maximum iterations without final resolution.")

    if verbose:
        print(f'\nUser prompt: "{user_prompt}"')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

