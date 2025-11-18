from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str | None = None
    JWT_KEY: str
    ALGORITHM: str
    
    class Config:
        env_file = ".env"
    
    @field_validator('DATABASE_URL', mode='before')
    def create_database_url(cls, field_value,  validation_info):
        if field_value is not None:
            return field_value
        other_fields = validation_info.data
        return f"postgresql+asyncpg://{other_fields['DB_USER']}:{other_fields['DB_PASS']}@{other_fields['DB_HOST']}:{other_fields['DB_PORT']}/{other_fields['DB_NAME']}"

settings = Settings()