from flask import Flask, request, jsonify
from test import Ultrawebhook
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# ✅ Database connection details (update these with your Hostinger credentials)
DB_CONFIG = {
    "host": "srv1006.hstgr.io",  # usually 'localhost' or your Hostinger DB host
    'user': 'u252854390_replies_user',
    'password': 'whatsapp_replies@321UltraMsg',
    'database': 'u252854390_whatsapp_reply'
}


# ✅ Save reply to MySQL
def save_reply_to_db(phone, message):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "REPLACE INTO replies (phone, message, created_at) VALUES (%s, %s, %s)"
        values = (phone, message, datetime.now())
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")


# ✅ Get reply from MySQL
def get_reply_from_db(phone):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT message FROM replies WHERE phone = %s", (phone,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['message'] if result else "No reply"
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Error fetching reply"


# ✅ Webhook route
@app.route("/", methods=["POST"])
def home():
    if request.json:
        bot = Ultrawebhook(request.json)
        result = bot.processing()

        message_data = request.json.get("data", {})
        if message_data:
            sender = message_data["from"]
            message = message_data["body"]
            save_reply_to_db(sender, message)

        return result


# ✅ Check reply via GET
@app.route("/check_reply/<phone_number>", methods=["GET"])
def check_reply(phone_number):
    reply = get_reply_from_db(phone_number)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
