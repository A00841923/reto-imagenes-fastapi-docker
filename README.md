# imagenes-fastapi — identidad e imágenes de referencia

El servidor de la Práctica 10 de TC2007B y punto de partida para el reto:
**FastAPI + PostgreSQL + RustFS**, con el mismo contrato que
`https://startdroid.com/api` (Prácticas 6 y 8) más las imágenes:

    POST /api/imagenes          (profesor) multipart `archivo` → { id, tipo, bytes }
    GET  /api/imagenes/:clave   (con sesión) la imagen, con ETag y caché de un año
    POST /api/avisos            { titulo, cuerpo, imagen? }

Las imágenes viven en un almacén de objetos compatible con S3 (RustFS); PostgreSQL
solo guarda su clave. Todo corre en Docker: la base, el almacén, el servidor y, si
lo pides, un túnel HTTPS.

    cp .env.example .env                   # y cambia los secretos
    docker compose up -d                   # http://localhost:8000/docs
    bash smoke.sh                          # los 31 casos del contrato, con sus códigos
    docker compose --profile tunel up -d   # el túnel; su dirección sale en:
    docker compose logs tunel

La consola del almacén: http://localhost:9001/rustfs/console/ (usuario y contraseña:
`S3_ACCESS_KEY` y `S3_SECRET_KEY` de tu `.env`).

`.env` nunca se sube al repositorio. `smoke.sh` lee de ahí el código de profesor.

La guía de lectura es el anexo del curso: https://startdroid.com/practicas/anexo-imagenes-docker

## Rama `calidad`: pruebas automatizadas

Esta rama agrega `tests/` (pytest) para la clase de calidad. Las pruebas corren
**dentro del contenedor**, contra la base y el almacén reales:

    git fetch ; git switch calidad
    docker compose up -d --build                  # la imagen ahora trae pytest
    docker compose exec api uv run --no-sync pytest

Al cambiar de rama hay que reconstruir (`--build`) porque cambiaron las dependencias.
Después, editar una prueba o el código de `app/` **no** requiere reconstruir: las dos
carpetas están montadas. Tu `.env` y tus datos se conservan.

| Archivo | Qué prueba |
| --- | --- |
| `tests/test_contrato.py` | Lo que ya funciona y no debe romperse (regresión) |
| `tests/test_permisos.py` | Tarjeta 1: quién puede borrar qué. **Una prueba falla a propósito** |
| `tests/test_duplicados.py` | Tarjeta 2: el mismo envío dos veces. Una prueba de caracterización y un contrato por diseñar |
| `tests/test_huerfanas.py` | Tarjeta 3: la imagen que queda sin aviso |

El registro del equipo está en `docs/registro-calidad.md`: llénenlo mientras trabajan.

Para correr solo una: `docker compose exec api uv run --no-sync pytest tests/test_permisos.py -v`
