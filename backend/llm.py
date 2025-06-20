import ollama
import re


def get_truck_status(truck_code: str) -> str:
    """
    Get status of truck from database

    Args:
      truck_code (str): The truck code

    Returns:
      str: Current status of the truck
    """
    dummy_db = {
        "TRUCK1234": "Delayed due to weather",
        "T456": "Delivered",
        "TRUCK789": "In Transit",
    }
    return dummy_db.get(truck_code.strip().upper(), "No status found for this truck.")


get_truck_status_tool = {
    "type": "function",
    "function": {
        "name": "get_truck_status",
        "description": "Get status of truck from database",
        "parameters": {
            "type": "object",
            "required": ["truck_code"],
            "properties": {
                "truck_code": {"type": "string", "description": "The truck code"},
            },
        },
    },
}


available_functions = {
    "get_truck_status": get_truck_status,
}


SYSTEM_PROMPT = """
You are a voice-based customer service agent helping users check only the status of their trucks.

Guidelines:
- Use a friendly, polite tone.
- Only speak like a human would in short, natural sentences unless using tools.
- DO NOT add extra information.
- DO NOT mention being an AI or a chatbot.
- DO NOT use emoji or any symbols that aren't a word.
- If you do not know the answer, just say you don't know.
- If no conversation history exists, start by asking the truck code.
- The code might be spaced try to decipher if cannot ask the user for the code again.
- If you do not understand the user reply politely ask user to repeat.
- You can only provide truck status if anyone asks other than that just say you cannot assist regarding anything other than truck status.
"""


def prompt_ollama(conversation):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation
    print("Prompting to ollama...")
    response = ollama.chat(
        model="qwen3", messages=messages, stream=False, tools=[get_truck_status_tool]
    )
    print("done")

    return response


def chat_with_ollama(conversation):
    response = prompt_ollama(conversation)
    reply_content = response["message"]["content"]

    print("Checking if tool is called...")
    if response.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_functions.get(tool.function.name):
                print("Calling function:", tool.function.name)
                print("Arguments:", tool.function.arguments)
                output = function_to_call(**tool.function.arguments)

                conversation.append(
                    {"role": "tool", "content": str(output), "name": tool.function.name}
                )

                print("Function output:", output)

                # Recurse to get the final human response
                print("Re-prompting with tool data...")
                response = prompt_ollama(conversation)
                reply_content = response["message"]["content"]
            else:
                print("Function", tool.function.name, "not found")

    # Final human-like reply
    conversation.append({"role": "assistant", "content": reply_content})
    return conversation
