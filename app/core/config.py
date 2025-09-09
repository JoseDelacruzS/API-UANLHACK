import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "API UANL Hack"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/uanl_hack_db")
    
    # External APIs Configuration
    API_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    # AI Model APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Other External APIs
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    MAPS_API_KEY: str = os.getenv("MAPS_API_KEY", "")
    
    # Cache settings (using local file cache)
    CACHE_DURATION: int = 300  # 5 minutes in seconds
    CACHE_DIR: str = os.getenv("CACHE_DIR", "./cache")
    
    # Conversation settings
    MAX_CONVERSATION_HISTORY: int = 100
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    
    class Config:
        case_sensitive = True

settings = Settings()
