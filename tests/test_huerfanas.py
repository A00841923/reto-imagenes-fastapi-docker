"""Tarjeta 3 · La imagen que nadie usa.

Publicar con imagen son dos peticiones: primero la imagen, después el aviso. Si la
segunda falla, la primera ya pasó. Esta prueba de caracterización demuestra lo que
queda en el almacén hoy.
"""

from fastapi.testclient import TestClient

from app import almacen

from .conftest import Persona


def test_hoy_si_el_aviso_falla_la_imagen_se_queda_en_el_almacen(cliente: TestClient, ana: Persona, subir):
    clave = subir(ana)

    # El aviso no pasa la validación del servidor (título de una letra).
    r = cliente.post("/api/avisos", headers=ana.headers, json={"titulo": "X", "cuerpo": "Un cuerpo válido para el aviso.", "imagen": clave})
    assert r.status_code == 422

    try:
        assert almacen.existe(clave), "La imagen ya no está en el almacén"
    finally:
        almacen.borrar(clave)  # la prueba limpia lo que dejó
