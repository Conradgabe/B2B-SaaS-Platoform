from fastapi import FastAPI
from app.root.routers import auth, tenants, clients, workflows

app = FastAPI(title="B2B SaaS Platform")

# Register routers
app.include_router(auth.router)
app.include_router(tenants.router)
app.include_router(clients.router)
app.include_router(workflows.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to B2B SaaS Platform API"}
