from pydantic_settings import BaseSettings
from pydantic import field_validator, AnyHttpUrl, validator
from typing import List, Optional, Union
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://shift_user:shift_password@localhost:5432/shift_planner"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    # Application
    APP_NAME: str = "Shift Planner API"
    DEBUG: bool = False
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                # JSON array
                return json.loads(v)
            # Comma-separated string
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return []
    
    class Config:
        env_file = ".env"


settings = Settings() 