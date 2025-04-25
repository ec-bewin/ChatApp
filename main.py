# main.py
from fastapi import FastAPI,Request,HTTPException
from user.urls import router as urls_router
from chat.urls import router as chat_router
from ws.urls import router as ws_router
from sqladmin import Admin
from user.admin import UserAdmin
from db import sync_engine
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from response import ErrorResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
logger = logging.getLogger(__name__)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return ErrorResponse(message="The requested resource was not found", status_code=404)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return ErrorResponse(message=exc.detail, status_code=exc.status_code)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return ErrorResponse(message="Internal server error", status_code=500)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    missing_fields = []
    for error in errors:
        if error["type"] == "missing": 
            field_name = error["loc"][-1]
            missing_fields.append(f"{field_name} is required")

    message = missing_fields[0] if missing_fields else "Invalid request data"

    return ErrorResponse(
        message=message
    )


#admin
admin = Admin(app, sync_engine, base_url="/admin",title="CHat App")
admin.add_view(UserAdmin)

#api/v1/
app.include_router(urls_router, prefix="/api/v1/users")
app.include_router(chat_router, prefix="/api/v1/chats")

connected_users = {}

@app.websocket("/ws/chats/")
async def websocket_endpoint( websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
          
            
    except:
      
     
        await websocket.close()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
