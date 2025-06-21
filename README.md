# Agentic-Helpdesk

The Agentic-Helpdesk is an AI-powered system designed to streamline emergency communication through automated SMS interactions using Twilio and Mistral AI. It processes and responds to messages with advanced AI, providing timely and accurate information during emergencies.

### Prerequisites
- install **ngrok**

### Setup Instructions
1. Clone the project
2. `pip install -r requirements.txt`
3. Add .env file
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+447123456789
MISTRAL_API_KEY=your_api_key_here
```

### Run the Application
1. Run app.py
`python app.py`
2. Start ngrok in a new terminal
`ngrok start sms`
3. Send a message from a new terminal
```
curl -X POST http://127.0.0.1:7860/api/v1/run/83527a4e-dc12-4171-b91d-b7d04ffb7a48 \
  -H "Content-Type: application/json" \
  -d '{"input_value": "hello", "input_type": "text", "output_type": "text"}'
```
4. Get the reply in the same terminal
5. Send a message from sms
6. Get the reply on your phone



### Workflow
```
[User sends SMS to Twilio number]
        ↓
Flask receives it at /sms (via Twilio webhook)
        ↓
Flask forwards message to Langflow
        ↓
Langflow returns AI-generated reply
        ↓
Flask responds to user using Twilio's MessagingResponse
```