# main.py
from fastapi import FastAPI
from user.urls import router as urls_router
from sqladmin import Admin
from user.admin import UserAdmin
from db import engine
app = FastAPI()


#admin
admin = Admin(app, engine, base_url="/admin",title="CHat App")
admin.add_view(UserAdmin)

#api/v1/
app.include_router(urls_router, prefix="/api/v1")


#
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
