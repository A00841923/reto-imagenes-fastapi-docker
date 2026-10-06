"""Tarjeta 2 · Envié una vez, aparecieron dos.

La primera prueba NO dice cómo debería ser el servidor: dice cómo ES hoy. Se llama
prueba de caracterización. Si su equipo implementa la protección contra duplicados,
va a fallar, y eso es bueno: hay que reescribirla con el contrato nuevo.

La segunda está apagada (skip). Es el contrato que su equipo tiene que diseñar.
Cuando lo acuerden, quiten el skip y ajústenla a lo que decidieron.
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from .conftest import Persona


def test_hoy_el_mismo_envio_dos_veces_crea_dos_avisos(ana: Persona, publicar):
    primero = publicar(ana, titulo="Feria de proyectos")
    segundo = publicar(ana, titulo="Feria de proyectos")

    assert primero["id"] != segundo["id"]


@pytest.mark.skip(reason="Tarjeta 2: primero acuerden el contrato (qué encabezado, qué responde el reintento, qué pasa si la clave llega con otro contenido)")
def test_reintentar_con_la_misma_clave_no_crea_otro_aviso(cliente: TestClient, ana: Persona):
    cuerpo = {"titulo": "Feria de proyectos", "cuerpo": "El viernes a las 12:00 en el patio central."}
    headers = {**ana.headers, "Idempotency-Key": str(uuid.uuid4())}

    primero = cliente.post("/api/avisos", headers=headers, json=cuerpo)
    reintento = cliente.post("/api/avisos", headers=headers, json=cuerpo)

    assert primero.status_code == 201
    assert reintento.json()["id"] == primero.json()["id"]
