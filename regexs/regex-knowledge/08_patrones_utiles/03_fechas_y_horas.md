# fechas_y_horas.md
Formatos comunes de fecha

Las fechas varían enormemente según la región. Los patrones más comunes incluyen:

    ISO 8601: YYYY-MM-DD (recomendado para sistemas)

    Europeo: DD/MM/YYYY

    EE.UU.: MM/DD/YYYY

    Formato largo: 12 de enero de 2024
    Cada uno requiere un patrón específico.

Patrón para fecha ISO estándar
regex

^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$

    Año: cuatro dígitos.

    Mes: 01-12.

    Día: 01-31 (no valida meses con menos días; esto es un problema).
    Limitación: Acepta 2023-02-31. Para validar días por mes se necesita una lógica más compleja, que puede hacerse con alternancia o condicionales en regex avanzadas, pero generalmente es mejor validar con código.

Validación estricta de fecha (incluyendo febrero)
regex

^(?:\d{4}-(?:(?:0[13578]|1[02])-31|(?:0[1,3-9]|1[0-2])-(?:29|30)|(?:0[1-9]|1\d|2[0-8])-(?:0[1-9]|1\d|2[0-8]))|(?:(?:\d{2}(?:0[48]|[2468][048]|[13579][26])|(?:[02468][048]|[13579][26])00)-02-29)$

Este patrón valida fechas en formato YYYY-MM-DD, incluyendo bisiestos para febrero. Es bastante ilegible; se recomienda usar código en su lugar.

Alternativa híbrida: usar una regex simple para el formato y luego una función para validar rangos.
python

import re
from datetime import datetime
def validar_fecha(texto):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', texto):
        try:
            datetime.strptime(texto, '%Y-%m-%d')
            return True
        except ValueError:
            pass
    return False

Fechas en formato DD/MM/YYYY o MM/DD/YYYY

    DD/MM/YYYY: ^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$
    (Con separadores / o - intercambiables usando grupo: [-/]).

    MM/DD/YYYY: ^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$
    Ninguno distingue entre meses de 30 o 31 días.

Horas en formato 24h y 12h

    24 horas: ^(?:[01]\d|2[0-3]):[0-5]\d$ (sin segundos)
    Con segundos: ^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$

    12 horas (AM/PM): ^(?:1[0-2]|0?[1-9]):[0-5]\d(?::[0-5]\d)?\s?[APap][Mm]$

Fecha y hora combinadas (ISO 8601 completo)
regex

^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$

Ejemplo: 2023-10-05T14:30:00Z, 2024-01-01T00:00:00+01:00.

    La parte decimal de segundos es opcional.

    Zona horaria Z o offset.

Extracción de fechas en texto libre

Para encontrar fechas en formato DD de Mes de YYYY (español), se puede usar:
regex

\b(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+(\d{4})\b

Grupos capturan día, mes y año.
Consideraciones de regionalización

    En aplicaciones web, se debe saber de antemano el formato esperado; no intentar adivinar entre múltiples formatos con una sola regex.

    Los nombres de meses y días de la semana son dependientes del idioma.

    Las regex son una herramienta de pre-validación; la validación final debe usar las funciones de fecha del lenguaje.
