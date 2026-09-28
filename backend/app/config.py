from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://crm:crm@postgres:5432/crm"
    keycloak_internal_url: str = "http://keycloak:8080"
    keycloak_public_url: str = "http://localhost:8081"
    keycloak_realm: str = "crm"
    keycloak_client_id: str = "crm-backend"
    keycloak_client_secret: str = "change_me"
    cors_origins: str = "http://localhost,http://localhost:3000"
    upload_dir: str = "/data/uploads"
    redis_url: str = "redis://redis:6379/0"
    max_upload_mb: int = 25
    auth_disabled: bool = False
    lms_api_url: str = ""
    lms_api_token: str = ""
    website_api_url: str = ""
    website_api_token: str = ""
    keycloak_admin: str = "admin"
    keycloak_admin_password: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def keycloak_issuer(self) -> str:
        return f"{self.keycloak_internal_url}/realms/{self.keycloak_realm}"

settings = Settings()
