# Registro de calidad · ¿Liberamos el servidor de Avisos mañana?

Un registro por equipo. Llénenlo mientras trabajan, no al final: es su evidencia.
Peguen lo que respondió el servidor y lo que dijo pytest tal cual, sin resumir.
Al terminar, entréguenlo donde les indique su profesor.

**Equipo:**
**Integrantes:**

---

## Subasta de riesgos

| Riesgo | Puntos |
| --- | ---: |
| Un profesor borra lo ajeno | |
| Avisos duplicados | |
| Imágenes huérfanas | |
| Interfaz inaccesible | |
| Lentitud | |
| **Total** | **10** |

**Nuestra mayor inversión y por qué** (impacto, probabilidad, costo de recuperación):

## Criterios de aceptación

Dado ___, cuando ___, entonces ___; lo verificaremos con ___.

1.
2.
3.

---

## Tarjeta 0 · La primera corrida

```text
(pega aquí la última línea de pytest)
```

---

## Tarjeta 1

**Roles** · teclado: · investigador de pruebas: · usuario: · relator:

**Identidad, datos y condiciones iniciales:**

**Petición para reproducir y lo que respondió el servidor:**

```text

```

**Resultado esperado:**

**La regla que se rompe, en una línea:**

**Dónde va la corrección (archivo y función), y por qué ahí y no en la app:**

**pytest antes de la corrección:**

```text

```

**pytest después de la corrección:**

```text

```

**El caso válido que comprobamos sigue funcionando:**

**Limitación o riesgo pendiente:**

### Revisión del otro equipo

**Equipo que nos revisó:**

**Pude observar ___; falta comprobar ___.**

---

## Tarjeta 2

**Roles** · teclado: · investigador de pruebas: · usuario: · relator:

**Lo que observamos al enviar dos veces:**

```text

```

**Por qué desactivar el botón no basta:**

**Nuestro contrato:**

- Cómo reconoce el servidor que es «la misma operación»:
- Qué responde al reintento:
- Qué pasa si la llave llega con otro contenido:
- Qué pasa si los dos envíos llegan al mismo tiempo:

**La prueba de `test_duplicados.py`, ajustada a nuestro contrato y sin el `skip` (pega el código y lo que dijo pytest):**

```python

```

```text

```

**Limitación o riesgo pendiente:**

---

## Tarjeta 3

**Roles** · teclado: · investigador de pruebas: · usuario: · relator:

**Lo que observamos (la clave de la imagen, el 422, y la imagen que sigue ahí):**

```text

```

**Quién se perjudica, y cuándo se nota (hoy, en un mes, en un año):**

**Nuestra política:** quién borra, cuándo, y cómo sabe que nadie usa la imagen:

**La prueba de cómo debería ser con nuestra política (pega el código; si no está implementada, escriban «sin implementar»):**

```python

```

**Limitación o riesgo pendiente:**

---

## Extensiones (si llegaron)

**Cuál hicimos y qué encontramos:**

---

## Comité de liberación

**Decisión:** liberar · liberar con una limitación explícita · detener *(dejen una)*

**Defecto más grave, a quién afecta y nuestra evidencia:**

**Lo que no comprobamos:**

**La razón de la decisión:**
