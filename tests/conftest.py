"""Lo que comparten todas las pruebas.

Las pruebas corren DENTRO del contenedor de la API, contra la base y el almacén de
verdad (los de docker compose). No hay versiones falsas de PostgreSQL ni de RustFS:
una prueba de permisos contra una base de mentira no demuestra que la real los respete.

Cada prueba crea sus propios usuarios con un sufijo al azar. Así no chocan entre sí
ni con lo que ya tengas en tu base, y se pueden correr las veces que quieras.

    docker compose exec api uv run --no-sync pytest
"""

import base64
import uuid
from collections.abc import Callable, Iterator
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

# Una imagen PNG válida de 2 x 2 píxeles. Basta para el servidor: revisa los primeros bytes.
PNG_CHICO = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAEElEQVR4nGPgi/ECIgYIBQASzgLRQRXuCAAAAABJRU5ErkJggg=="
)


@dataclass
class Persona:
    """Alguien con sesión: su usuario, su rol y su token de acceso."""

    usuario: str
    rol: str
    token: str

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}


@pytest.fixture(scope="session")
def cliente() -> Iterator[TestClient]:
    """La API, en el mismo proceso que la prueba. Sin red de por medio.

    El `with` corre el arranque del servidor (crea las tablas y el bucket), igual
    que cuando se levanta con uvicorn.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def registrar(cliente: TestClient) -> Callable[..., Persona]:
    """Crea una cuenta nueva y devuelve quién es. Con rol="profesor", usa tu CODIGO_PROFESOR."""

    def _registrar(nombre: str, rol: str = "alumno") -> Persona:
        usuario = f"{nombre}.{uuid.uuid4().hex[:8]}"
        cuerpo = {"usuario": usuario, "password": "secreta123"}
        if rol == "profesor":
            cuerpo["codigoProfesor"] = settings.codigo_profesor
        r = cliente.post("/api/auth/register", json=cuerpo)
        assert r.status_code == 201, r.text
        assert r.json()["rol"] == rol
        return Persona(usuario=usuario, rol=rol, token=r.json()["accessToken"])

    return _registrar


# Las tres personas del caso. Ana y Bruno son profesores; Carla es alumna.
@pytest.fixture
def ana(registrar: Callable[..., Persona]) -> Persona:
    return registrar("ana", "profesor")


@pytest.fixture
def bruno(registrar: Callable[..., Persona]) -> Persona:
    return registrar("bruno", "profesor")


@pytest.fixture
def carla(registrar: Callable[..., Persona]) -> Persona:
    return registrar("carla")


@pytest.fixture
def publicar(cliente: TestClient) -> Callable[..., dict]:
    """Publica un aviso como `quien` y devuelve lo que respondió el servidor. Exige 201."""

    def _publicar(quien: Persona, titulo: str = "Aviso de prueba", cuerpo: str = "Cuerpo de un aviso de prueba.", **extra) -> dict:
        r = cliente.post("/api/avisos", headers=quien.headers, json={"titulo": titulo, "cuerpo": cuerpo, **extra})
        assert r.status_code == 201, r.text
        return r.json()

    return _publicar


@pytest.fixture
def subir(cliente: TestClient) -> Callable[[Persona], str]:
    """Sube una imagen chica como `quien` y devuelve su clave. Exige 201."""

    def _subir(quien: Persona) -> str:
        r = cliente.post("/api/imagenes", headers=quien.headers, files={"archivo": ("prueba.png", PNG_CHICO, "image/png")})
        assert r.status_code == 201, r.text
        return r.json()["id"]

    return _subir
