# Manejo de Fechas y Horas con Regex

## Formatos Comunes de Fecha

Las fechas varían enormemente según la región. Los patrones más comunes que un desarrollador debe manejar incluyen:

*   **ISO 8601**: `YYYY-MM-DD` (recomendado para sistemas y bases de datos).
*   **Europeo**: `DD/MM/YYYY`.
*   **EE.UU.**: `MM/DD/YYYY`.
*   **Formato largo**: `12 de enero de 2024`.

Cada uno requiere un patrón específico para su correcta identificación.

## Validación de Fechas

### 1. Patrón para Fecha ISO estándar

```regex
^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$
```

*   **Año**: Cuatro dígitos.
*   **Mes**: `01-12`.
*   **Día**: `01-31`.

> [!WARNING]
> **Limitación**: Este patrón acepta fechas inválidas como `2023-02-31`. Para validar días por mes se necesita una lógica más compleja o validación post-regex.

### 2. Validación estricta (Incluyendo Febrero y Bisiestos)

```regex
^(?:\d{4}-(?:(?:0[13578]|1[02])-31|(?:0[1,3-9]|1[0-2])-(?:29|30)|(?:0[1-9]|1\d|2[0-8])-(?:0[1-9]|1\d|2[0-8]))|(?:(?:\d{2}(?:0[48]|[2468][048]|[13579][26])|(?:[02468][048]|[13579][26])00)-02-29)$
```

> [!TIP]
> Este patrón valida fechas en formato `YYYY-MM-DD`, incluyendo bisiestos para febrero. Debido a su complejidad e ilegibilidad, **se recomienda usar funciones nativas del lenguaje** para la validación final.

### 3. Alternativa Híbrida (Recomendada)

Usar una regex simple para el formato y luego una función para validar la lógica temporal.

```python
import re
from datetime import datetime

def validar_fecha(texto):
    # Validar formato básico
    if re.match(r'^\d{4}-\d{2}-\d{2}$', texto):
        try:
            # Validar lógica de fecha (días, meses, bisiestos)
            datetime.strptime(texto, '%Y-%m-%d')
            return True
        except ValueError:
            pass
    return False
```

## Formatos Regionales

*   **DD/MM/YYYY**: `^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$`
    *(Para permitir separadores `/` o `-` intercambiables, usar un grupo: `[-/]`)*.
*   **MM/DD/YYYY**: `^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$`

> [!NOTE]
> Estos patrones básicos no distinguen entre meses de 30 o 31 días.

## Horas en Formato 24h y 12h

*   **24 horas**: `^(?:[01]\d|2[0-3]):[0-5]\d$` (sin segundos).
*   **24 horas con segundos**: `^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$`.
*   **12 horas (AM/PM)**: `^(?:1[0-2]|0?[1-9]):[0-5]\d(?::[0-5]\d)?\s?[APap][Mm]$`.

## Fecha y Hora combinadas (ISO 8601 completo)

```regex
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$
```

**Ejemplos válidos:**
* `2023-10-05T14:30:00Z`
* `2024-01-01T00:00:00+01:00`

*   La parte decimal de segundos es opcional.
*   Soporta zona horaria `Z` (UTC) o *offset* numérico.

## Extracción de Fechas en Texto Libre

Para encontrar fechas en formato "DD de Mes de YYYY" (español):

```regex
\b(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+(\d{4})\b
```

> [!TIP]
> Los grupos capturan por separado: `1. Día`, `2. Mes`, `3. Año`.

## Consideraciones de Regionalización

*   **Anticipación**: En aplicaciones web, se debe conocer de antemano el formato esperado; no es recomendable intentar adivinar entre múltiples formatos con una sola regex.
*   **Idioma**: Los nombres de meses y días de la semana dependen totalmente del idioma configurado.
*   **Pre-validación**: Las regex son excelentes para pre-validar o extraer; la validación final de "existencia" de la fecha debe delegarse a bibliotecas especializadas.

---

[« Anterior](02_urls.md) | [Siguiente »](04_numeros_y_monedas.md)

