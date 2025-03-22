from flask import Flask, request, jsonify
from test import Ultrawebhook
import json

app = Flask(__name__)

# JSON file to store the last replies
DATA_FILE = "replies.json"


# Function to load data from JSON file
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Function to save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Webhook route to receive WhatsApp messages
@app.route("/", methods=["POST"])
def home():
    if request.json:
        bot = Ultrawebhook(request.json)
        result = bot.processing()

        # Extract message details
        message_data = request.json.get("data", {})
        if message_data:
            sender = message_data["from"]
            message = message_data["body"]

            # Save last message reply
            saved_data = load_data()
            saved_data[sender] = message
            save_data(saved_data)

        return result


# ✅ New route: Check reply status
@app.route("/check_reply/<phone_number>", methods=["GET"])
def check_reply(phone_number):
    saved_data = load_data()

    # ✅ Ensure that the number matches the stored format
    formatted_number = f"{phone_number}@c.us"

    print(f"🔍 Checking for number: {formatted_number}")  # Debugging Print
    print(f"📂 Saved Data: {saved_data}")  # Debugging Print

    reply = saved_data.get(formatted_number, "No reply")
    print(f"✅ Reply Found: {reply}")  # Debugging Print

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
