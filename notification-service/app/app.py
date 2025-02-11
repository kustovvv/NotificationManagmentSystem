from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .notification_api import *

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5005)
