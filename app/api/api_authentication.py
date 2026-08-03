import os
from fastapi import HTTPException, Request
from twilio.request_validator import RequestValidator


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


class AuthenticationVerifier:
    @classmethod
    async def verify_twilio_credentials(cls, request: Request):
        form_data = await request.form()
        account_sid =  form_data.get("AccountSid")

        cls.verify_account_sid(account_sid)
        twilio_signature = request.headers.get("X-Twilio-Signature")
        cls.has_twilio_signature(twilio_signature)
        cls.is_correct_signature(request, form_data, twilio_signature)

    @classmethod
    def has_twilio_signature(cls, twilio_signature):
        print("verifying_if_has_signature...")
        if not twilio_signature:
            raise HTTPException(
                status_code=403,
                detail="Unnauthorized: No Twilio Signature"
            )
    
    @classmethod
    def is_correct_signature(cls, request, form_data, twilio_signature):
        params = dict(form_data)
        url = str(request.url)
        validator = RequestValidator(TWILIO_AUTH_TOKEN)
        is_valid = validator.validate(
            uri=url,
            params=params,
            signature=twilio_signature
        )
        if not is_valid:
            raise HTTPException(403, "Unnauthorized: Invalid Twilio Signature")
    

    @classmethod
    def verify_account_sid(cls, account_sid):
        if account_sid != TWILIO_ACCOUNT_SID:
            raise HTTPException(401, "Invalid SID Data")
            