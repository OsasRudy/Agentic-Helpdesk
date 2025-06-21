import os
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import requests
import logging
from rag import retrieve_info  # Import the RAG function

# Load from .env file
load_dotenv()

# Set up Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

app = Flask(_name_)

# Incident data
INCIDENTS = [
    {"area": "Downtown", "incident": "fire",
     "instructions": "Evacuate via Main Street. Do not use elevators. Contact Fire Services at 101."},
    {"area": "Harbour", "incident": "flood",
     "instructions": "Move to higher ground. Avoid low-lying areas. Contact 102 for rescue services."}
]

@app.route("/sms", methods=["POST"])
def sms():
    url = "http://127.0.0.1:7861/api/v1/run/83527a4e-dc12-4171-b91d-b7d04ffb7a48"

    # 1. Receive the message from users
    sender = request.form.get("From", "")
    msg = request.form.get('Body', '').strip()
    logging.info(f"Received SMS from {sender}: {msg}")

    # 2. Use RAG to retrieve relevant information
    retrieved_info = retrieve_info(msg)
    augmented_message = f"{msg} {retrieved_info}"

    # 3. Check if any area matches the message
    for incident in INCIDENTS:
        if incident["area"].lower() in msg.lower():
            resp = MessagingResponse()
            reply = f"We got {incident['incident']} at {incident['area']} from {sender}"
            resp.message(reply)
            resp.message("✅ Message received. Working on it...")

            # 4. Send the augmented message to Langflow
            payload = {
                "input_value": augmented_message,
                "output_type": "text",
                "input_type": "text"
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                # Send API request
                response = requests.post(url, json=payload, headers=headers)
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

            resp.message(ai_reply)
            return str(resp)

    # No area match
    resp = MessagingResponse()
    resp.message("❗ Sorry, we couldn't find incident info for your area.")
    return str(resp)

if _name_ == "_main_":
    app.run(debug=True)