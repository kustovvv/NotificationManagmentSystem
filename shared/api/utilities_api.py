from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

def standard_response(success: bool, message: str, data=None, status_code: int = 200):
    print('message: ', message)
    return JSONResponse(content={"success": success, "message": message, "data": data}, status_code=status_code)

