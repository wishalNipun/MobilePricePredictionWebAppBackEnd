from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

class MobileForm(BaseModel):
    brand: str
    color: str
    model: str
    memory: str
    storage: str

@app.post("/featureMobile")
async def submit_mobile_form(mobile_data: MobileForm):
    # Access the submitted data using mobile_data
    brand = mobile_data.brand
    color = mobile_data.color
    model = mobile_data.model
    memory = mobile_data.memory
    storage = mobile_data.storage

    # Perform any necessary processing or validation here
    
    # Return a response (you can customize this based on your requirements)
    return {"message": "Form data submitted successfully", "data": mobile_data.dict()}