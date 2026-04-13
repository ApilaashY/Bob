import ollama
import function
import re
import shlex

from dotenv import load_dotenv
load_dotenv(".env")

# Seperate function to get prompt to update as more tools are added
def getPrompt():
    functions = function.getFunctions()
    available_functions = "\n".join(str(f) for f in functions)

    system_prompt = f"""You are an AI assistant that follows the ReAct (Reasoning and Acting) architecture.
    Your goal is to help the user by breaking down tasks into logical steps.

    For each turn, you should follow this structure:
    Thought: Describe your reasoning about the current state and what you should do next.
    Action: If you need to perform an action, specify the function to call in the format: <function_name> <param1> <param2> ...
    Observation: (This will be provided to you after you call an action)
    Final Answer: Once you have all the information or have completed the task, provide the final response to the user.

    CRITICAL RULES:
    1. You MUST always start with a "Thought:".
    2. If you need to call a function, use exactly one "Action:" line. Do not include extra text on the Action line.
    3. If you have the final answer, use "Final Answer:".
    4. Do NOT make up observations. Wait for the system to provide them.
    5. Only use the functions provided below.
    6. If you need to write a list as a parameter for a function call, write the list in the format of a python list surrounded by quotations without commas. Example: \"[1 2 3]\" or \"['a' 'b' 'c']\"
    7. For the createFunction function, the parameters should have the same format as the avaliable functions given later, i.e. in the format name:type. Using rule 6, an example of a create function call would be: auto.createFunction "search" "google" "Searches the web for a given query." ["query:string"]
    8. Try to not use the search ability and instead create function to get the information you need. You should try to prioritize getting results to the user directly from yourself and not through the search function.

    Available functions:
    {available_functions}

    Action Format:
    Action: <function_name> <param1> <param2> ...
    (Do not include parameter names, <, >, or quotes. Just the values separated by spaces.)

    EXAMPLES:

    User: find the movie Interstellar
    Thought: I need to find the movie Interstellar and open it. I will use the einthusan.findandget function.
    Action: einthusan.findandget Interstellar
    Observation: Movie found and opened.
    Thought: The movie has been opened successfully. I can now provide the final answer.
    Final Answer: I have found and opened the movie Interstellar for you.

    User: hi
    Thought: The user is greeting me. I will respond with a friendly greeting and ask how I can help.
    Final Answer: Hello! How can I help you today?
    """
    return system_prompt

model = 'llama3.1:latest'

logs = [{'role': 'system', 'content': getPrompt()}]
prompt = ""

# Keep asking user for prompts
while prompt != "\\bye":

    prompt = ""
    while prompt.strip() == "":
        prompt = input("\nYou: ")

    if prompt == "\\bye":
        break

    logs.append({'role': 'user', 'content': prompt})

    while True:
        logs[0]['content'] = getPrompt()
        stream = ollama.chat(
            model=model,
            messages=logs,
            stream=True,
            options={'temperature': 0.0}
        )

        print(f"--- Response from {model} ---")
        full_response = ""
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            print(content, end='', flush=True)
        print("\n-----------------------------")

        # Record assistant's response in logs
        logs.append({'role': 'assistant', 'content': full_response})

        # Parse for Action
        action_match = re.search(r"Action:\s*(.*)", full_response, re.IGNORECASE)
        final_answer_match = re.search(r"Final Answer:\s*(.*)", full_response, re.IGNORECASE)

        if action_match:
            action_line = action_match.group(1).strip()
            
            if input(f"EXECUTE? (y/n): ").lower() == 'y':
                parts = shlex.split(action_line, posix=False)
                func_name = parts[0]
                func_args = parts[1:]
                
                result = "Function not found"
                for f in function.getFunctions():
                    if f.name == func_name:
                        result = f.execute(func_args)
                        break
                
                if result is None:
                    result = "Success"
                
                print(f"Observation: {result}")
                logs.append({'role': 'user', 'content': f"Observation: {result}"})
                # Loop continues to let model process observation
            else:
                logs.append({'role': 'user', 'content': "Observation: User cancelled the action."})
                break # Or should it continue? Usually break if user cancels.
        
        elif final_answer_match:
            # Task complete
            break
        else:
            # Fallback if model didn't use tags correctly
            break



