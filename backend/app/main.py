from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .models import *  # Import all models to register them
from .api import auth, organizations, employees, shift_patterns, schedules, leaves

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="A modern shift scheduling automation system"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["Organizations"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(shift_patterns.router, prefix="/api/shift-patterns", tags=["Shift Patterns"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["Schedules"])
app.include_router(leaves.router, prefix="/api/leaves", tags=["Leaves"])


@app.get("/")
async def root():
    return {"message": "Welcome to Shift Planner API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 