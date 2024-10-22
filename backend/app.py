from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from chat import Chatbot
from openai import OpenAI


# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    """Handles the chat interaction with GPT-4."""
    data = request.get_json()
    user_message = data.get("message")
    chatbot = Chatbot(client)
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    conversation = [{"role": "user", "content": user_message}]
    
    try:
        assistant_reply = chatbot.chat_with_gpt(user_message)['Assistant']
        conversation.append({"role": "assistant", "content": assistant_reply})

        # Save the conversation locally
        # save_conversation(conversation)

        return jsonify({"reply": assistant_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5151)
