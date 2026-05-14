from twilio.rest import Client
from django.conf import settings


# =========================
# PHONE NUMBER FORMATTER
# =========================
def format_phone_number(phone):
    """
    Converts Indian numbers to Twilio E.164 format
    Example:
    0749800XXXX -> +91749800XXXX
    749800XXXX -> +91749800XXXX
    """

    phone = str(phone).strip().replace(" ", "")

    # Remove starting 0
    if phone.startswith("0"):
        phone = phone[1:]

    # Add country code if missing
    if not phone.startswith("+91"):
        phone = "+91" + phone

    return phone


# =========================
# ORDER SMS FUNCTION
# =========================
def send_order_sms(phone_number, order_id, total_amount):

    try:

        # Format phone number
        formatted_phone = format_phone_number(
            phone_number
        )

        # Twilio client
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        # Send SMS
        message = client.messages.create(
            body=(
                f"eShop: Your order #{order_id} has been placed successfully.\n"
                f"Total Amount: ₹{total_amount}\n"
                f"Thank you for shopping with us!"
            ),
            from_=settings.TWILIO_PHONE_NUMBER,
            to=formatted_phone
        )

        print("SMS SENT SUCCESS:", message.sid)

        return message.sid

    except Exception as e:

        print("SMS Error:", e)

        return None