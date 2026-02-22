from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ciao dal cluster k3s!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/info")
def info():
    return {
        "app": "k8s-lab",
        "version": "1.0.0",
        "description": "La mia prima app su Kubernetes"
    }
@app.get("/saluta/{nome}")
def saluta(nome: str):
    return {"messaggio": f"Ciao {nome}, benvenuto nel cluster k3s!"}
