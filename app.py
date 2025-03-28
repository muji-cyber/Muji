from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from config import apikey

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for frontend-backend communication

# Configure the API key for Google Generative AI
API_KEY = apikey
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    # Get the user message from the request
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    concise_question = f"Mujahid programmed you: {user_message}"

    try:
        # Send the user message to the chatbot
        response = chat.send_message(concise_question)
        if response.candidates:
            bot_reply = response.candidates[0].content.parts[0].text
            return jsonify({'reply': bot_reply})
        else:
            return jsonify({'reply': 'Sorry, I couldn\'t understand your question.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
