"""Application configuration, read from environment variables (12-factor).

Every setting can be overridden by an env var of the same name, e.g.
``DATABASE_URL``. The defaults target the local docker-compose stack.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "VNS Research Platform API"
    # 'db' is the service name in docker-compose; override for other setups.
    database_url: str = "postgresql+psycopg2://vns:vns@db:5432/vns"


settings = Settings()
