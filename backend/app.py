import re
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from whisper_handler import transcribe_audio
from tts_handler import synthesize_speech  # returns bytes
from llm import chat_with_ollama  # returns conversation history with last reply

app = Flask(__name__)

CORS(app)


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
        conversation = chat_with_ollama(conversation)
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


# Static file serving for default audio
@app.route("/static/<filename>")
def serve_static(filename):
    return send_file(f"static/{filename}", mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)
