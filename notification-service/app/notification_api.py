from fastapi import Request, HTTPException
from dotenv import load_dotenv

from .notification_service import NotificationService
from shared.api.utilities_api import standard_response, decode_jwt_token
from .app import app

load_dotenv()
notification_service = NotificationService()

@app.post("/send_notification")
async def send_notification(request: Request):
    try:
        data = await request.json()
        jwt_token = request.headers.get('authorization')            
        user_id = await decode_jwt_token(jwt_token)

        return standard_response(success=True, message="Notification sent successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
