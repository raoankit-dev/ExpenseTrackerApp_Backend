from fastapi import FastAPI

app = FastAPI(
    title="Expense Tracking App",
    description="Backend API for an AI-powered Expense Tracker",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "msg":"Welcome to expense tracking app."
    }

@app.get("/health")
def health_check():
    return {
        "status":"healthy"
    }