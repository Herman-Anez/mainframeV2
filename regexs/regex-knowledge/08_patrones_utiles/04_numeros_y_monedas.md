# numeros_y_monedas.md
Números enteros y decimales básicos

    Entero (positivo y negativo): ^-?\d+$

    Decimal con punto: ^-?\d+\.\d+$

    Decimal con posible parte decimal opcional: ^-?\d+(?:\.\d+)?$

    Notación científica: ^-?\d+(?:\.\d+)?[eE][+-]?\d+$

Números con separadores de miles

Formato estándar con coma para miles y punto decimal (ej. 1,234.56):
regex

^-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$

Variante con espacio como separador de miles y coma decimal (ej. 1 234,56):
regex

^-?\d{1,3}(?:[ ]\d{3})*(?:,\d{2})?$

Combinando ambos (poco común) se puede permitir tanto coma como punto mediante un patrón más complejo.
Monedas con símbolo

    Dólar/euro con símbolo prefijo: ^\$\s?-?\d+(?:\.\d{2})?$ o ^[€$]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$

    Símbolo al final (ej. 100€): ^\d+(?:\.\d{2})?\s?[€$]$

    Con código de moneda: ^[A-Z]{3}\s?\d+(?:\.\d{2})?$

Extracción flexible de cantidades monetarias en texto
regex

(?:[\$\€\£]|USD|EUR)?\s?\d{1,3}(?:[,.]\d{3})*(?:\.\d{2})?(?:\s?(?:€|USD))?

Esto captura cantidades como $1,000.50, 2000 EUR, 3.500,75 € (con formato europeo, pero se confundiría con separador de miles). La ambigüedad entre millares y decimales puede resolverse con un patrón más inteligente que detecte el último punto/coma como decimal.

Patrón que supone que el último separador especial es el decimal:
regex

[-+]?\d{1,3}(?:[.,]\d{3})*[.,]\d{2}\b

Pero fallaría si no hay decimales. Para cantidades sin decimales: \b\d{1,3}(?:[.,]\d{3})+\b (sin decimales).
Porcentajes
regex

^-?\d+(?:\.\d+)?%$

O con restricción de rango 0-100: no es práctico con regex pura; mejor validar después.
Validaciones adicionales

    No permitir ceros a la izquierda (excepto el número 0 o 0.xx): ^(?:0|[1-9]\d*)(?:\.\d+)?$

    Números negativos precisos: el signo menos solo al inicio.

Optimizaciones y compatibilidad

    Todos estos patrones funcionan en cualquier motor con pequeñas adaptaciones (escapado de $, uso de \d).

    Para aplicaciones financieras, valida la cantidad con regex y después conviértela a un tipo numérico para comprobar límites.

    No uses regex para sumas o comparaciones, solo para formato.

Ejemplos prácticos

Python: extraer todos los precios en euros de un texto
python

import re
pat = r'(\d{1,3}(?:\.\d{3})*,\d{2})\s?€|\d{1,3}(?:,\d{3})*\.\d{2}\s?EUR'
precios = re.findall(pat, texto)

JavaScript: validar número de teléfono (aunque no es moneda) y monedas
javascript

const moneyRegex = /^\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$/;
moneyRegex.test("$1,234.56"); // true
