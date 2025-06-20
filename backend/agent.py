import re
from typing import Literal, List, Dict
from flask import json
import ollama

AGENT_TYPES = Literal["enquiry_agent"]

SYSTEM_CONTEXT = """
You are a voice-based customer service agent helping users check the status of their trucks.

Guidelines:
- Use a friendly, polite tone.
- Speak like a human would in short, natural sentences.
- DO NOT add extra information.
- DO NOT ask questions outside the given list.
- DO NOT mention being an AI or a chatbot.
- Stick to the provided script.

Function Call Syntax:
Use the format:
  $$function_name(argument1, argument2, ...)$$

Only respond with the function call (not the user-facing message). The function result will be passed to you in the next turn to phrase naturally.

Supported Functions:
- get_truck_status(truck_code1, truck_code2, ...)
"""

AGENTS: Dict[str, str] = {
    "enquiry_agent": """
Step 1: Greet the user and ask for their name and the truck code.
Step 2: From the user's response, extract one or more truck codes and return:
         $$get_truck_status(truck_code1, truck_code2, ...)$$
Step 3: Given the truck status of each truck (e.g. "loading", "transit"), respond to the user naturally.
"""
}

FUNC_PATTERN = re.compile(r"\$\$(\w+)\s*\((.*?)\)\$\$")


# Simulated truck status fetcher
def get_truck_status(truck_code: str) -> str:
    # Mock logic (customize as needed)
    sample_statuses = ["loading", "transit", "stopped", "delivered"]
    return sample_statuses[hash(truck_code) % len(sample_statuses)]


def format_messages(history, agent_script, system_prompt, extra_context=""):
    context = f"""
{system_prompt}

Conversation Script:
{agent_script}

Current Conversation Progress:
{json.dumps(history, indent=2)}
""".strip()

    if extra_context:
        context += f"\n\n{extra_context.strip()}"

    messages = [{"role": "system", "content": context}]
    for pair in history:
        if pair.get("question"):
            messages.append({"role": "assistant", "content": pair["question"].strip()})
        if pair.get("answer"):
            messages.append({"role": "user", "content": pair["answer"].strip()})
    return messages


def handle_conversation(history: List[Dict[str, str]], agent: AGENT_TYPES) -> str:
    if agent not in AGENTS:
        raise ValueError(f"Unsupported agent type: {agent}")

    agent_script = AGENTS[agent]

    # First LLM call to detect function call
    messages = format_messages(history, agent_script, SYSTEM_CONTEXT)
    response_1 = ollama.chat(model="gemma3", messages=messages)
    model_output = response_1["message"]["content"].strip()

    # Check if function call is present
    match = FUNC_PATTERN.search(model_output)
    if match:
        func_name, param_str = match.group(1), match.group(2).strip()
        if func_name == "get_truck_status":
            # Split truck codes and trim whitespace
            truck_codes = [
                code.strip() for code in param_str.split(",") if code.strip()
            ]

            # Get status for each
            results = [(code, get_truck_status(code)) for code in truck_codes]

            # Format context as a clean table
            status_context = "| Truck Code | Status |\n|------------|--------|\n"
            status_context += "\n".join(
                f"| {code} | {status} |" for code, status in results
            )

            # Second call to phrase final response using the context
            messages = format_messages(
                history, agent_script, SYSTEM_CONTEXT, status_context
            )
            print(messages)
            response_2 = ollama.chat(model="gemma3", messages=messages)
            return response_2["message"]["content"].strip()

        return f"[Unsupported function: {func_name}]"

    return model_output
