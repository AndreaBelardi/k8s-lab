from fastapi import FastAPI
import os

app = FastAPI()

ENVIRONMENT = os.getenv("ENVIRONMENT", "unknown")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
SECRET_KEY = os.getenv("SECRET_KEY", "not-set")

@app.get("/")
def root():
    return {
        "message": "Ciao dal cluster k3s!",
        "status": "ok",
        "environment": ENVIRONMENT
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/info")
def info():
    return {
        "app": "k8s-lab",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "secret_configured": SECRET_KEY != "not-set"
    }

@app.get("/saluta/{nome}")
def saluta(nome: str):
    return {"messaggio": f"Ciao {nome}, benvenuto nel cluster k3s!"}
