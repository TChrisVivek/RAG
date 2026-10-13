from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.agent import router as agent_router
from app.services.tools import get_employee_info

print(get_employee_info("EMP001"))
print(get_employee_info("EMP002"))
print(get_employee_info("EMP003"))

app = FastAPI()

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "message": "HR Policy Assistant API is running!"
    }