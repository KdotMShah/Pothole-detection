from twilio.rest import Client

def Alert():
    # Twilio credentials (replace these with your own)
    account_sid = ''
    auth_token = ''
    twilio_whatsapp_number = ''  # Twilio sandbox number
    recipient_whatsapp_number = ''

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send WhatsApp message
    message = client.messages.create(
        body="Pothole(s) detected, drive cautiously!",
        from_=twilio_whatsapp_number,
        to=recipient_whatsapp_number
    )

    print(f"WhatsApp message sent with SID: {message.sid}")