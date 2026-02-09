from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agentic FMCG Intelligence Platform")

app.include_router(router)

# Run:
# uvicorn app.main:app --reload
