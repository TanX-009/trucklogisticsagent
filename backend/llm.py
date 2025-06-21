import ollama


def prompt_ollama(system_prompt, conversation, tools):
    messages = [{"role": "system", "content": system_prompt}] + conversation
    print("Prompting to ollama...")
    response = ollama.chat(model="qwen3", messages=messages, stream=False, tools=tools)
    print("done")

    return response


def chat_with_ollama(
    system_prompt, conversation, tool_kit, reprompt_after_toolcall=True
):
    response = prompt_ollama(system_prompt, conversation, tool_kit["tools"])
    reply_content = response["message"]["content"]
    print("response----------------------")
    print(response)
    print("response----------------------")

    print("Checking if tool is called...")
    if response.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := tool_kit["available_functions"].get(
                tool.function.name
            ):
                print("Calling function:", tool.function.name)
                print("Arguments:", tool.function.arguments)
                output = function_to_call(**tool.function.arguments)

                conversation.append(
                    {"role": "tool", "content": str(output), "name": tool.function.name}
                )

                print("Function output:", output)

                # Recurse to get the final human response
                if reprompt_after_toolcall:
                    print("Re-prompting with tool data...")
                    response = prompt_ollama(
                        system_prompt, conversation, tool_kit["tools"]
                    )
                    reply_content = response["message"]["content"]
            else:
                print("Function", tool.function.name, "not found")

    # Final human-like reply
    conversation.append({"role": "assistant", "content": reply_content})
    return conversation
