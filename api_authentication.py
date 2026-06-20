import os
from fastapi import HTTPException, Request
from twilio.request_validator import RequestValidator


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


#TODO -> Split it in more functions 
class AuthenticationVerifier:

    @classmethod
    async def verifySID(cls, request: Request):
        form_data = await request.form()
        account_sid =  form_data.get("AccountSid")

        if account_sid != TWILIO_ACCOUNT_SID:
            raise HTTPException(401, "Invalid Authentication Data")
        
        twilio_signature = request.headers.get("X-Twilio-Signature")
        if not twilio_signature:
            raise HTTPException(
                status_code=403,
                detail="Unnauthorized: No Twilio Signature"
            )
        
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