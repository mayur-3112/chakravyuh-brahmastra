from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Chakravyuh-Brahmastra"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    SCAN_TIMEOUT: int = 300
    MAX_CONCURRENT_SCANS: int = 5
    DEFAULT_PORT_RANGE: str = "1-1000"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    REPORT_DIR: Path = BASE_DIR / "reports"
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"

settings = Settings()
settings.LOG_DIR.mkdir(exist_ok=True)
settings.REPORT_DIR.mkdir(exist_ok=True)
