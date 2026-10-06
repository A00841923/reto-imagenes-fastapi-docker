"""Lo que ya funciona y no debe romperse.

Todas estas pasan desde el primer día. Su trabajo no es arreglar nada: es avisar
el día que alguien rompa una regla sin darse cuenta. Eso es una prueba de regresión.
"""

from fastapi.testclient import TestClient

from .conftest import Persona


def test_sin_token_responde_401_con_la_forma_del_contrato(cliente: TestClient):
    r = cliente.get("/api/avisos")

    assert r.status_code == 401
    # La app de Android lee `error`; con {"detail": ...} mostraría un mensaje genérico.
    assert r.json()["code"] == "falta_token"
    assert "error" in r.json()


def test_un_token_alterado_no_sirve(cliente: TestClient, carla: Persona):
    # Se cambia un carácter de la firma. Quien no conoce JWT_SECRET no puede firmar otro.
    encabezado, datos, firma = carla.token.split(".")
    otra_firma = ("A" if firma[0] != "A" else "B") + firma[1:]

    r = cliente.get("/api/avisos", headers={"Authorization": f"Bearer {encabezado}.{datos}.{otra_firma}"})

    assert r.status_code == 401
    assert r.json()["code"] == "token_invalido"


def test_una_alumna_no_puede_publicar(cliente: TestClient, carla: Persona):
    r = cliente.post("/api/avisos", headers=carla.headers, json={"titulo": "Hola", "cuerpo": "Esto no debe publicarse nunca."})

    assert r.status_code == 403


def test_lo_que_publica_una_profesora_aparece_en_el_tablon(cliente: TestClient, ana: Persona, carla: Persona, publicar):
    aviso = publicar(ana, titulo="Examen parcial")

    tablon = cliente.get("/api/avisos", headers=carla.headers).json()

    assert aviso["id"] in [a["id"] for a in tablon]
    assert aviso["autor"] == ana.usuario  # el autor lo pone el servidor, no el cliente


def test_un_titulo_de_puros_espacios_no_se_guarda(cliente: TestClient, ana: Persona):
    r = cliente.post("/api/avisos", headers=ana.headers, json={"titulo": "     ", "cuerpo": "El título está vacío aunque no lo parezca."})

    assert r.status_code == 422
    assert r.json()["field"] == "titulo"
    # Y no quedó nada a medias: Ana no tiene ningún aviso.
    tablon = cliente.get("/api/avisos", headers=ana.headers).json()
    assert ana.usuario not in [a["autor"] for a in tablon]
