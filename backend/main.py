from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .pipeline import Pipeline
import uvicorn
import os
import traceback

app = FastAPI(title="AI Assessment Generator")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == "backend":
    FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
else:
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

pipeline = Pipeline()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')

@app.get("/index.html")
async def read_index():
    return FileResponse('frontend/index.html')

class GenerateRequest(BaseModel):
    grade: int
    topic: str

@app.post("/generate")
async def generate_content(request: GenerateRequest):
    print(f"Received generation request for Grade {request.grade}, Topic: {request.topic}")
    try:
        result = pipeline.run(request.grade, request.topic)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
