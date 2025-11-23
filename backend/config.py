"""
Configuration validation and management for IPL Oracle backend
"""
import os
import sys
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    """Raised when configuration is invalid or missing"""
    pass


class Config:
    """Application configuration with validation"""
    
    # Pinecone configuration
    PINECONE_API_KEY: str
    PINECONE_REGION: str
    PINECONE_CLOUD: str
    INDEX_NAME: str = "ipl-players"
    
    # Gemini configuration
    GEMINI_API_KEY: Optional[str]
    
    # Environment
    ENV: str
    PORT: int
    
    @classmethod
    def load(cls) -> None:
        """Load and validate configuration from environment variables"""
        errors = []
        
        # Required: Pinecone configuration
        cls.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
        if not cls.PINECONE_API_KEY:
            errors.append("PINECONE_API_KEY is required")
            
        cls.PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
        cls.PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
        
        # Optional: Gemini API (backend can work without it)
        cls.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not cls.GEMINI_API_KEY:
            print("⚠️  GEMINI_API_KEY not set. AI responses will be limited.", file=sys.stderr)
        
        # Environment settings
        cls.ENV = os.getenv("ENV", "development")
        cls.PORT = int(os.getenv("PORT", "8000"))
        
        if errors:
            error_msg = "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ConfigError(error_msg)
        
        # Log configuration (without sensitive values)
        print("✅ Configuration loaded:")
        print(f"   Environment: {cls.ENV}")
        print(f"   Port: {cls.PORT}")
        print(f"   Pinecone Region: {cls.PINECONE_REGION}")
        print(f"   Pinecone Cloud: {cls.PINECONE_CLOUD}")
        print(f"   Index Name: {cls.INDEX_NAME}")
        print(f"   Gemini API: {'✓' if cls.GEMINI_API_KEY else '✗'}")


# Load configuration on module import
try:
    Config.load()
except ConfigError as e:
    print(f"❌ {e}", file=sys.stderr)
    sys.exit(1)
