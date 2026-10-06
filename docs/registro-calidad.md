# Registro de calidad · ¿Liberamos el servidor de Avisos mañana?

**Un registro por equipo.** Es lo único que se entrega. Llénenlo mientras trabajan, no al final.

Cada sección corresponde a una diapositiva, y sus puntos numerados son los mismos
que dice **«Entreguen»** en esa diapositiva. Donde dice *pega*, copien la salida tal
cual sale en la terminal o en `/docs`, sin resumir.

## Qué se entrega

| Sección | Qué | |
| --- | --- | --- |
| A · Riesgos y criterios | La subasta y tres criterios | Obligatorio |
| B · Tarjeta 1 | Los cuatro puntos y la revisión del otro equipo | Obligatorio |
| C · Tarjeta 2 | Puntos 1 y 2. El 3, si llegan | Obligatorio |
| D · Tarjeta 3 | Puntos 1 y 2. El 3, si llegan | Obligatorio |
| E · Comité | La decisión y su razón | Obligatorio |
| F · Extensiones | Lo que hayan hecho | Opcional |

**Equipo:**
**Integrantes:**

---

## A · Riesgos y criterios

**La subasta** (10 puntos en total):

| Riesgo | Puntos |
| --- | ---: |
| Un profesor borra lo ajeno | |
| Avisos duplicados | |
| Imágenes huérfanas | |
| Interfaz inaccesible | |
| Lentitud | |

**Por qué pusimos más puntos en ___:** (impacto, probabilidad, costo de recuperación)

**Tres criterios**, uno por cada riesgo con más puntos: *Dado ___, cuando ___, entonces ___; lo verificaremos con ___.*

1.
2.
3.

---

## B · Tarjeta 1 · Tengo sesión y tengo rol… ¿pero es mío?

**Roles:** teclado · investigador de pruebas · usuario · relator →

**1 · La reproducción en `/docs`.** Quién (Ana o Bruno), qué petición, y pega lo que respondió el servidor.

```text

```

**2 · La regla que se rompe, en una línea.**

**3 · Dónde va la corrección** (archivo y función), **y por qué ahí y no en la app.**

**4 · pytest antes y después.** El «antes» es la corrida de la Tarjeta 0 (`1 failed, 9 passed, 1 skipped`). Pega la última línea del «después», al terminar esta tarjeta: tiene que ser `10 passed, 1 skipped`.

```text

```

**Lo que nos dijo el equipo que nos revisó**, con su frase: *«Pude observar ___; falta comprobar ___»*

---

## C · Tarjeta 2 · Envié una vez, aparecieron dos

**Roles:** teclado · investigador de pruebas · usuario · relator →

**1 · Por qué desactivar el botón mientras envía no basta.**

**2 · El contrato.**

- Cómo reconoce el servidor que es «la misma operación»:
- Qué responde al reintento:
- Qué hace si la llave llega con otro contenido:

**3 · La prueba de `test_duplicados.py`, ajustada a su contrato y sin el `skip`.** Pega el código y la última línea de pytest (tiene que fallar: nadie lo ha implementado).

```python

```

---

## D · Tarjeta 3 · La imagen que nadie usa

**Roles:** teclado · investigador de pruebas · usuario · relator →

**1 · Quién se perjudica, y cuándo se nota:** hoy, en un mes, en un año.

**2 · Su política:** quién borra, cuándo, y cómo sabe que nadie usa la imagen.

**3 · La prueba de cómo debería ser con su política.** Pega el código. Si no la implementaron, escriban «sin implementar».

```python

```

---

## E · Comité de liberación

**Decisión** (dejen una): liberar · liberar con una limitación explícita · detener

**La razón, citando su evidencia de B, C o D:**

**Lo que no comprobaron:**

---

## F · Extensiones (opcional)

**Cuál hicieron y qué encontraron:**
