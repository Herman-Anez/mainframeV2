# Validación de Números y Monedas con Regex

## Números Enteros y Decimales Básicos

Los siguientes patrones cubren los casos de uso numéricos más fundamentales:

*   **Entero (positivo y negativo)**: `^-?\d+$`
*   **Decimal con punto**: `^-?\d+\.\d+$`
*   **Decimal con parte opcional**: `^-?\d+(?:\.\d+)?$`
*   **Notación científica**: `^-?\d+(?:\.\d+)?[eE][+-]?\d+$`

## Números con Separadores de Miles

### 1. Formato Anglosajón
Coma para miles y punto para decimales (ej. `1,234.56`):
```regex
^-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$
```

### 2. Formato Europeo/Internacional
Espacio como separador de miles y coma para decimales (ej. `1 234,56`):
```regex
^-?\d{1,3}(?:[ ]\d{3})*(?:,\d{2})?$
```

> [!NOTE]
> Combinar ambos en un solo patrón es posible pero poco común, ya que suele preferirse establecer un estándar por aplicación o región.

## Monedas con Símbolo

Dependiendo de la ubicación del símbolo y el formato del número:

*   **Símbolo prefijo (Dólar/Euro)**: `^\$\s?-?\d+(?:\.\d{2})?$` o `^[€$]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$`
*   **Símbolo sufijo (ej. 100€)**: `^\d+(?:\.\d{2})?\s?[€$]$`
*   **Código de moneda (ISO)**: `^[A-Z]{3}\s?\d+(?:\.\d{2})?$`

## Extracción Flexible de Cantidades en Texto

Para capturar precios dentro de un párrafo ignorando la ambigüedad inicial:

```regex
(?:[\$\€\£]|USD|EUR)?\s?\d{1,3}(?:[,.]\d{3})*(?:\.\d{2})?(?:\s?(?:€|USD))?
```

> [!CAUTION]
> Esto captura cantidades como `$1,000.50`, `2000 EUR`, o `3.500,75 €`. La ambigüedad entre millares y decimales puede ser un problema si el texto mezcla formatos regionales.

### Estrategia de "Último Separador"
Patrón que supone que el último separador especial es el decimal:
```regex
[-+]?\d{1,3}(?:[.,]\d{3})*[.,]\d{2}\b
```

## Porcentajes

```regex
^-?\d+(?:\.\d+)?%$
```

> [!TIP]
> Si necesitas restringir el rango (ej. 0-100), no es práctico hacerlo con regex pura; es mucho más eficiente validar el formato con regex y el rango con lógica de programación.

## Validaciones Adicionales y Buenas Prácticas

*   **Evitar ceros a la izquierda**: `^(?:0|[1-9]\d*)(?:\.\d+)?$` (Permite `0` o `0.xx`, pero no `0123`).
*   **Precisión de Negativos**: Asegúrate de que el signo menos solo se permita al inicio absoluto de la cadena.

> [!IMPORTANT]
> **Regla de Oro**: No utilices regex para realizar cálculos, comparaciones de magnitud o sumas. Úsalas exclusivamente para validar el **formato visual** y extraer los datos.

## Ejemplos Prácticos

### Python: Extraer precios en euros
```python
import re

pat = r'(\d{1,3}(?:\.\d{3})*,\d{2})\s?€|\d{1,3}(?:,\d{3})*\.\d{2}\s?EUR'
precios = re.findall(pat, texto)
```

### JavaScript: Validar moneda
```javascript
const moneyRegex = /^\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$/;
moneyRegex.test("$1,234.56"); // true
```

---

[« Anterior](03_fechas_y_horas.md) | [Siguiente »](05_contrasenas.md)

