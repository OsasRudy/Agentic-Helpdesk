import os
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import requests

# Load from .env file
load_dotenv()

# Set up Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

app = Flask(__name__)

# Endpoint to receive SMS 
@app.route("/get-sms", methods=["POST"])
def receive_sms():
    msg = request.form['Body']
    sender = request.form['From']

    resp = MessagingResponse()
    # resp.message(f"Message: {msg}")
    print(f"Received SMS from {sender}: {msg}")
    return str(resp)


# Endpoint to send SMS
@app.route("/send-sms", methods=["POST"])
def send_sms():
    to = request.form['to']
    body = request.form['body']

    message = client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to=to
    )
    return f"Sent message SID: {message.sid}"

# Endpoint
@app.route("/sms", methods=["POST"])
def sms():
    # 1. Receive the message from users
    msg = request.form['Body']
    sender = request.form['From']

    # 2. Send the message to your Langflow flow and get the reply
    url = "http://127.0.0.1:7860/api/v1/run/83527a4e-dc12-4171-b91d-b7d04ffb7a48"

    payload = {
        "input_value": msg,
        "output_type": "text",
        "input_type": "text"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send API request
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        langflow_msg = response.json()
        # Extract the AI reply safely
        ai_reply = (
            langflow_msg.get("outputs", [{}])[0]
                .get("outputs", [{}])[0]
                .get("results", {})
                .get("text", {})
                .get("data", {})
                .get("text", "Sorry, I didn’t get that.")
        )
    except Exception as e:
        print("Langflow error:", e)
        ai_reply = "Sorry, there was a problem getting the response."

    # 3. Send the AI reply back to the user via Twilio
    resp = MessagingResponse()
    resp.message(ai_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)