from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationBufferMemory


# Define your truck status tool function
def get_truck_status(truck_code: str) -> str:
    # Replace with real DB lookup
    dummy_db = {
        "TRUCK1234": "Delayed due to weather",
        "TRUCK456": "Delivered",
        "TRUCK789": "In Transit",
    }
    return dummy_db.get(truck_code.strip().upper(), "No status found for this truck.")


# Define the LangChain tool
tools = [
    Tool(
        name="TruckStatusTool",
        func=get_truck_status,
        description="Useful when you need to find the status of a truck. Input should be a truck code.",
    )
]

# Base system prompt
SYSTEM_CONTEXT = """
You are a voice-based customer service agent helping users check the status of their trucks.

Guidelines:
- Use a friendly, polite tone.
- Speak like a human would in short, natural sentences.
- DO NOT add extra information unless retrieved from a tool(e.g. TruckStatusTool).
- DO NOT mention being an AI or a chatbot.
- DO NOT try to make up an answer.
"""

# Instantiate Ollama model
llm = ChatOllama(
    model="mistral",
    temperature=0.5,  # or any other model name available in your Ollama
)

# Memory for maintaining chat context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the agent with tool calling
agent: AgentExecutor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    agent_kwargs={"system_message": SYSTEM_CONTEXT},
)


# Function to be used by Flask
def chat_with_ollama(history: list[dict]) -> str:
    # Add messages to memory before running
    memory.clear()
    for item in history:
        if item["role"] == "user":
            memory.chat_memory.add_user_message(item["content"])
        elif item["role"] == "assistant":
            memory.chat_memory.add_ai_message(item["content"])
    # Ask the last user message again
    last_user_msg = [msg["content"] for msg in history if msg["role"] == "user"][-1]
    response = agent.run(last_user_msg)
    return response
