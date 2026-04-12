import ollama
import function
import sys

model = 'llama3.1:latest'
prompt = "Give me a small greeting"
functions = function.getFunctions()
available_functions = "\n".join(str(f) for f in functions)

system_prompt = f"""You are an AI assistant that can perform actions using the available functions.
You are the orchestrational part; you will say what function to execute, and a program will execute it for you.

CRITICAL FORMATTING RULES:
Every response MUST ALWAYS consist of at least two lines.
Line 1 MUST be the exact function call, or exactly NONE if no function is needed.
Line 2 and onwards MUST be your response to the user or a description of what you still have to do.
NEVER start Line 1 with conversational text like "I would like to execute:". Just the function call or NONE.

Available functions:
{available_functions}

Function Call Format:
<function_name> <param1> <param2> ...
(Do not include the parameter names, <, >, or quotes. Just provide the values separated by spaces in the right order.)

EXAMPLES:

User: find the movie Interstellar
Assistant Response:
einthusan.findandget Interstellar
I will search for the movie Interstellar and open it for you.

User: open youtube
Assistant Response:
google.open https://www.youtube.com
Opening YouTube for you.

User: hi
Assistant Response:
NONE
Hello! How can I help you today?
"""

logs = [{'role': 'system', 'content': system_prompt}]

# Keep asking user for prompts
while prompt != "\\bye":

    prompt = ""
    while prompt.strip() == "":
        prompt = input("\nYou: ")

    logs.append({'role': 'user', 'content': prompt})

    stream = ollama.chat(
        model=model,
        messages=logs,
        stream=True,
        options={'temperature': 0.0}
    )

    print(f"--- Response from {model} ---")
    full_output = ""
    output = ""
    command = ""
    for chunk in stream:
        chunk_content = chunk['message']['content']
        full_output += chunk_content
        output += chunk_content
        
        if command == "":
            if "\n" in output:
                command = output.split("\n")[0].strip()
                output = "\n".join(output.split("\n")[1:])

            # REMOVE THIS LATER
            print(chunk_content, end='', flush=True)
        else:
            print(chunk_content, end='', flush=True)
    
    # Detect if there is only one line
    if command == "" and "\n" not in output:
        command = output
        output = ""
        

    print("\n-----------------------------")
    print("COMMAND: ", command)

    if (command != "NONE"):
        if (input("EXECUTE?(y): ") == "y"):
            command_parts = command.split(" ")
            function_name = command_parts[0]
            function_params = command_parts[1:]
        
            for function in functions:
                if function.name == function_name:
                    function.execute(function_params)
                    break

    # Append the full output so the model sees its own valid history format
    logs.append({'role': 'assistant', 'content': full_output})


