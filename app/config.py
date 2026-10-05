from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Todo lo que cambia entre tu máquina y el servidor vive en el entorno, no en el código.

    Se lee de variables de entorno o de un archivo `.env` (que nunca se sube al repo).
    Si falta `JWT_SECRET` o `CODIGO_PROFESOR`, la app no arranca — a propósito.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/avisos"
    jwt_secret: str
    codigo_profesor: str

    # Cinco minutos de acceso y siete días de refresco: los mismos números de la Práctica 6.
    access_ttl_s: int = 5 * 60
    refresh_ttl_s: int = 7 * 24 * 60 * 60

    # El almacén de objetos (RustFS, compatible con S3). Las imágenes viven ahí, no en PostgreSQL.
    # Dentro de Docker se llama `almacen`; docker-compose.yml pone S3_ENDPOINT.
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str = "avisos"

    # Lo más grande que se acepta. La app de la Práctica 10 manda ~300 KB; una foto sin comprimir, 4 MB o más.
    imagen_max_bytes: int = 2 * 1024 * 1024


settings = Settings()
