import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from shared.logger.logger import logger

load_dotenv()

def standard_response(success: bool, message: str, data=None, status_code: int = 200):
    logger.debug(f"Standard response: {message}")
    return JSONResponse(content={"success": success, "message": message, "data": data}, status_code=status_code)

async def decode_jwt_token(jwt_token: str) -> str:
    try:
        if jwt_token.startswith('Bearer '):
            jwt_token = jwt_token.split('Bearer ')[1]
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://auth-service:5001/decode_token",
                json={"jwt_token": jwt_token.strip()},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
                
            response_data = response.json()
            if not response_data.get("success"):
                raise HTTPException(status_code=401, detail=response_data.get("message"))
                
            return response_data["data"]["user_id"]
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to decode token: {str(e)}")
