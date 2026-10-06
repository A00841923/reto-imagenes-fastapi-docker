# La imagen del servidor: Python 3.12 y las dependencias exactas de uv.lock.
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.12.9 /uv /bin/uv

WORKDIR /code
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

# Primero las dependencias: si solo cambia tu código, Docker reutiliza esta capa
# y reconstruir tarda segundos, no minutos. Con el grupo dev: pytest y httpx, para
# correr las pruebas dentro del contenedor (docker compose exec api uv run --no-sync pytest).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
