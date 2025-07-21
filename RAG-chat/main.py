# backend/main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def ping():
    return {"msg": "Hello from rag‑chat!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # nosec
