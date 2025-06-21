import re
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database import create_customer
from whisper_handler import transcribe_audio
from tts_handler import synthesize_speech  # returns bytes
from llm import chat_with_ollama  # returns conversation history with last reply
from tools import enquiry_agent_tool_kit, leadfinder_agent_tool_kit

app = Flask(__name__)

CORS(app)

ENQUIRY_AGENT_SYSTEM_PROMPT = """
You are a voice-based customer service agent helping users check only the status of their trucks.

Guidelines:
- Use a friendly, polite tone.
- Only speak like a human would in short, natural sentences unless using tools.
- DO NOT add extra information.
- DO NOT mention being an AI or a chatbot.
- DO NOT use emojis or any symbols that aren't a word or would sound weird when spoken.
- DO NOT quote anything.
- If you do not know the answer, just say you don't know.
- If no conversation history exists, start by asking the truck code.
- The code might be spaced try to decipher and strip the spaces if cannot ask the user for the code again.
- If you do not understand the user, ask the user to repeat politely.
- You can only provide truck status if anyone asks other than that just say you cannot assist regarding anything other than truck status.
- Ask user after answering for any other truck status enquiries.
- Only when user ends the conversation (thanking is also to be considered as end of conversation) reply with following at the end on a new line: $$end_conversation$$
"""


@app.route("/enquiry_agent", methods=["POST"])
def enquiry_agent():
    try:
        conversation_json = request.form.get("conversation")

        if not conversation_json:
            return jsonify({"error": "Missing conversation history"}), 400

        conversation = eval(conversation_json)

        # Start of conversation
        if len(conversation) == 0:
            starter_text = "Hello! Could you please tell me your truck code?"
            starter_audio = synthesize_speech(starter_text)
            encoded_audio = base64.b64encode(starter_audio).decode("utf-8")
            return jsonify(
                {
                    "conversation": [{"role": "assistant", "content": starter_text}],
                    "audio_base64": encoded_audio,
                    "end_conversation": False,
                }
            )

        # Audio file expected for ongoing conversation
        audio_file = request.files.get("audio")
        if not audio_file:
            return jsonify({"error": "Missing audio file"}), 400

        # Transcribe and append
        user_input = transcribe_audio(audio_file)
        conversation.append({"role": "user", "content": user_input})

        # Model response
        conversation = chat_with_ollama(
            ENQUIRY_AGENT_SYSTEM_PROMPT, conversation, enquiry_agent_tool_kit
        )
        raw_reply = conversation[-1]["content"]

        print("Detecting end of conversation...")
        # Post-process reply
        end_conversation = "$$end_conversation$$" in raw_reply
        cleaned_reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL)
        cleaned_reply = (
            cleaned_reply.replace("$$end_conversation$$", "").strip().replace("\n", " ")
        )

        # Update final assistant reply with cleaned version
        conversation[-1]["content"] = cleaned_reply

        # Convert to speech
        reply_audio_bytes = synthesize_speech(cleaned_reply)
        encoded_audio = base64.b64encode(reply_audio_bytes).decode("utf-8")

        return jsonify(
            {
                "conversation": conversation,
                "audio_base64": encoded_audio,
                "end_conversation": end_conversation,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


LEADFINDER_AGENT_SYSTEM_PROMPT = """
You are Neerja you work and call for and from X Logistics.
You are a voice-based logistics outreach agent conducting a short survey call with users.

Your goal is to collect the following 3 pieces of information from the user:
1. Do you currently transport any goods?
2. How much weight (in kg) do you usually transport?
3. From where to where do you transport goods?
4. Do you use transport services, partner with someone, or own trucks?

Guidelines:
- Ask these questions one by one.
- Be polite and sound natural, as if you're having a casual human conversation.
- DO NOT answer anything unrelated.
- DO NOT mention being an AI or a chatbot.
- Do NOT include any symbols or formatting that sound unnatural when spoken.
- If user says they are not interested or says thank you, politely end the conversation.
- If you don't understand, ask the user to repeat.
- After collecting all 3 answers or when user ends the conversation, reply with a polite "thank you for the information and have a great day" message and at the end on new line add following: $$end_conversation$$
- After receiving each answer from the user, use the tools to add the relevant data to relevant database using relevant tool.
"""


@app.route("/test", methods=["GET"])
def test():
    conversation = chat_with_ollama(
        "",
        [
            {
                "role": "system",
                "content": "user_id: 165bd217-78c5-434b-9605-90332e1d7397",
            },
            {"role": "user", "content": "I transport goods."},
        ],
        leadfinder_agent_tool_kit,
        reprompt_after_toolcall=False,
    )
    print("conversation--------------------")
    print(conversation)
    print("conversation--------------------")
    return "I transport goods."


@app.route("/leadfinder_agent", methods=["POST"])
def leadfinder_agent():
    try:
        conversation_json = request.form.get("conversation")
        customer_id = request.form.get("customer_id")

        if not conversation_json:
            return jsonify({"error": "Missing conversation history"}), 400

        conversation = eval(conversation_json)

        # Start of conversation
        if len(conversation) == 0 or not customer_id:
            starter_text = "Hello! I am Neerja speaking from X logistics. May I ask you a few questions?"

            customer_id = create_customer()

            starter_audio = synthesize_speech(starter_text)
            encoded_audio = base64.b64encode(starter_audio).decode("utf-8")
            return jsonify(
                {
                    "customer_id": customer_id,
                    "conversation": [
                        {"role": "system", "content": f"customer_id: {customer_id}"},
                        {"role": "assistant", "content": starter_text},
                    ],
                    "audio_base64": encoded_audio,
                    "end_conversation": False,
                }
            )

        # Audio file expected for ongoing conversation
        audio_file = request.files.get("audio")
        if not audio_file:
            return jsonify({"error": "Missing audio file"}), 400

        # Transcribe and append
        user_input = transcribe_audio(audio_file)
        conversation.append({"role": "user", "content": user_input})

        # Model response
        conversation = chat_with_ollama(
            LEADFINDER_AGENT_SYSTEM_PROMPT,
            conversation,
            leadfinder_agent_tool_kit,
        )
        raw_reply = conversation[-1]["content"]

        print("Detecting end of conversation...")
        # Post-process reply
        end_conversation = "$$end_conversation$$" in raw_reply
        cleaned_reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL)
        cleaned_reply = (
            cleaned_reply.replace("$$end_conversation$$", "").strip().replace("\n", " ")
        )

        # Update final assistant reply with cleaned version
        conversation[-1]["content"] = cleaned_reply

        # Convert to speech
        reply_audio_bytes = synthesize_speech(cleaned_reply)
        encoded_audio = base64.b64encode(reply_audio_bytes).decode("utf-8")

        return jsonify(
            {
                "customer_id": customer_id,
                "conversation": conversation,
                "audio_base64": encoded_audio,
                "end_conversation": end_conversation,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Static file serving for default audio
@app.route("/static/<filename>")
def serve_static(filename):
    return send_file(f"static/{filename}", mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)
