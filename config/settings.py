from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

class Settings(BaseSettings):
    # General application settings
    APP_NAME: str = "Enterprise RAG System"
    DEBUG: bool = False
    
    # Path settings
    # Default to a directory named "data" in the project's root
    # The project root is assumed to be the parent of the 'config' directory.
    # If this script is in /app/config/settings.py, then project_root is /app/
    # For a typical project structure where settings.py is in /config at the root,
    # Path(__file__).resolve().parent.parent / "data" would be correct.
    # Let's assume the script is run from the project root or that paths in .env are relative to root.
    # Pydantic's Path will resolve it relative to the CWD if a relative path is given.
    # We can also make it absolute.
    
    # To make it relative to the project root (assuming config/settings.py)
    # PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    # DATA_STORE_PATH: Path = PROJECT_ROOT / "data"
    
    # Simpler approach: Pydantic's Path type will handle relative paths based on CWD.
    # If DATA_STORE_PATH is set in .env as a relative path, it's relative to where the app is run.
    # If not set, it defaults to "data" relative to CWD.
    DATA_STORE_PATH: Path = Path("data")

    # API Key Management (example, can be expanded)
    OPENAI_API_KEY: str = "your_openai_api_key_here" # Default, should be overridden by .env

    # Database URL (example)
    DATABASE_URL: str = "sqlite:///./app_data.db" # Default, should be overridden by .env

    # Vector Store Path (can be a subdirectory of DATA_STORE_PATH or separate)
    # This makes it relative to DATA_STORE_PATH by default.
    VECTOR_STORE_SUBDIR: str = "vector_stores" 

    # Knowledge Base temporary file storage (can be a subdirectory of DATA_STORE_PATH)
    KB_TEMP_SUBDIR: str = "knowledge_bases_temp"


    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",                # Load .env file
        env_file_encoding='utf-8',      # Encoding for .env file
        extra='ignore',                 # Ignore extra fields from .env
        # case_sensitive=False,         # Uncomment if env vars might be mixed case (e.g. Windows)
    )

    # Derived path properties
    @property
    def VECTOR_STORE_PATH(self) -> Path:
        return self.DATA_STORE_PATH / self.VECTOR_STORE_SUBDIR

    @property
    def KNOWLEDGE_BASE_TEMP_PATH(self) -> Path:
        return self.DATA_STORE_PATH / self.KB_TEMP_SUBDIR

settings = Settings()

if __name__ == "__main__":
    print(f"Application Name: {settings.APP_NAME}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"OpenAI API Key (Loaded): {'********' if settings.OPENAI_API_KEY != 'your_openai_api_key_here' else 'Not Set or Default'}")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    print(f"\n--- Path Configurations ---")
    print(f"Raw DATA_STORE_PATH: {settings.DATA_STORE_PATH}")
    
    # Resolve and print absolute path for DATA_STORE_PATH
    # This ensures we see where 'data' is expected relative to the current working directory
    # if it's a relative path.
    abs_data_store_path = settings.DATA_STORE_PATH.resolve()
    print(f"Resolved DATA_STORE_PATH: {abs_data_store_path}")
    print(f"  Is absolute: {settings.DATA_STORE_PATH.is_absolute()}")
    
    print(f"Derived VECTOR_STORE_PATH: {settings.VECTOR_STORE_PATH.resolve()}")
    print(f"Derived KNOWLEDGE_BASE_TEMP_PATH: {settings.KNOWLEDGE_BASE_TEMP_PATH.resolve()}")

    # Example of how to ensure paths exist (optional, can be done at app startup)
    # settings.DATA_STORE_PATH.mkdir(parents=True, exist_ok=True)
    # settings.VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
    # settings.KNOWLEDGE_BASE_TEMP_PATH.mkdir(parents=True, exist_ok=True)
    # print(f"\nEnsured base data directories exist (if they didn't).")

    print(f"\nTo test with environment variables, create a .env file with, for example:")
    print(f"DATA_STORE_PATH=./my_custom_data_location")
    print(f"OPENAI_API_KEY=your_real_api_key")
    print(f"DATABASE_URL=postgresql://user:pass@host:port/dbname")
