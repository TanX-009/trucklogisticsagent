import ollama
import re


def get_truck_status(truck_code: str) -> str:
    dummy_db = {
        "TRUCK1234": "Delayed due to weather",
        "T456": "Delivered",
        "TRUCK789": "In Transit",
    }
    return dummy_db.get(truck_code.strip().upper(), "No status found for this truck.")


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
- DO NOT use tool when last message was from tool
- You can only provide truck status if anyone asks other than that just say you cannot provide anything else other than truck status.

Tools:
- To get truck status, reply ONLY with following:
$$get_truck_status TRUCK_CODE$$
- When user ends the conversation (thanking is also to be considered as end of conversation) reply with following at the end on a new line:
$$end_conversation$$
"""


def extract_truck_code(text):
    """Extract truck code from the LLM response with multiple fallback patterns"""

    # Pattern 1: Standard format $$get_truck_status CODE$$
    match = re.search(r"\$\$get_truck_status\s+([^\$]+?)\$\$", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Pattern 2: Handle missing spaces or extra characters
    match = re.search(r"\$\$get_truck_status([^\$]+?)\$\$", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Pattern 3: Handle single $ instead of $$
    match = re.search(r"\$get_truck_status\s+([^\$]+?)\$", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Pattern 4: Find any truck-like code pattern (fallback)
    # This looks for common truck code patterns
    match = re.search(r"\b(TRUCK\s*\d+|T\s*\d+|[A-Z]{2,}\s*\d+)\b", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return None


def prompt_ollama(conversation):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation
    print("Prompting to ollama...")
    response = ollama.chat(model="qwen3", messages=messages, stream=False)
    print("done")
    reply_content = response["message"]["content"]
    return reply_content


def chat_with_ollama(conversation):
    reply_content = prompt_ollama(conversation)

    print("Extracting truck code...")
    # Try to extract truck code
    truck_code = extract_truck_code(reply_content)

    if truck_code:
        print(f"Truck code: {truck_code}")
        # Clean up the truck code (remove spaces, convert to uppercase)
        clean_code = re.sub(r"\s+", "", truck_code.upper())
        status = get_truck_status(clean_code)

        conversation.append(
            {"role": "tool", "content": f"Truck Code: {clean_code} | Status: {status}"}
        )

        # Recurse to get the final human response
        print("Re-prompting with tool data...")
        reply_content = prompt_ollama(conversation)

    # Final human-like reply
    conversation.append({"role": "assistant", "content": reply_content})
    return conversation
