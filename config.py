from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Requisito 5b: Propriedades obrigatórias
    AMBIENTE: str = "desenvolvimento"
    LOG_LEVEL: str = "INFO"
    
    # Requisito 5b: Variáveis de Database (devem estar no seu .env)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Requisito 5 e 5a: Herança e leitura do .env
    model_config = SettingsConfigDict(env_file=".env")

    # Requisito 5c: Método para controle do Swagger
    def is_swagger_enabled(self) -> bool:
        return self.AMBIENTE.lower() != "producao"

settings = Settings()