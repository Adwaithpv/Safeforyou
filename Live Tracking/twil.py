from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC619558cccd05513004566158cff8fcf3"
AUTH_TOKEN = "400989aa84287153861d96c2e80a81c4"
TWILIO_PHONE_NUMBER = "+19526792789"
TO_PHONE_NUMBER = "+919880010184"

# Initialize Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Send message
message = client.messages.create(
    body="Works ig",
    from_=TWILIO_PHONE_NUMBER,
    to=TO_PHONE_NUMBER
)

print(f"Message sent! SID: {message.sid}")
