# Operadores y Coerción

## Operadores Principales

| Categoría | Operadores |
| :--- | :--- |
| **Aritméticos** | `+`, `-`, `*`, `/`, `%`, `**` (exponenciación) |
| **Asignación** | `=`, `+=`, `-=`, `*=`, `/=`, etc. |
| **Comparación** | `==`, `!=`, `===`, `!==`, `>`, `<`, `>=`, `Ratio <=` |
| **Lógicos** | `&&`, `||`, `??` (*nullish coalescing*) |
| **Ternario** | `condición ? valorVerdadero : valorFalso` |
| **Unarios** | `!`, `++`, `--`, `typeof`, `void`, `delete` |
| **Relacionales** | `in`, `instanceof` |

---

## Coerción de Tipos

La coerción es la conversión automática o manual de un tipo a otro.

### Coerción Explícita (Recomendada)

Se realiza mediante funciones nativas para asegurar el tipo de dato:

*   **`String(valor)`**: Convierte a cadena de texto.
*   **`Number(valor)`**, **`parseInt()`**, **`parseFloat()`**: Conversión a números.
*   **`Boolean(valor)`**: Conversión a booleano.
*   **`BigInt(valor)`**: Conversión a enteros de precisión arbitraria.
*   **`Symbol(valor)`**: Creación de símbolos.

---

### Coerción Implícita

Muchos operadores fuerzan la conversión de forma automática. Reglas básicas:

1.  **Suma (`+`)**:
    *   Si algún operando es `string`, el otro se convierte a `string` y se concatenan.
    *   En otro caso, ambos se convierten a `number` (si es posible) y se suman.
    *   `null` se convierte a `0`, `undefined` a `NaN` en contexto numérico.
2.  **Otros Aritméticos (`-`, `*`, `/`, etc.)**: Ambos operandos se convierten a `number`.
3.  **Comparación Débil (`==`)**:
    > [!WARNING]
    > Compara sin verificar el tipo, aplicando un algoritmo complejo de coerción. Si los tipos son distintos, fuerza la conversión de uno o ambos lados. **Se recomienda evitar su uso y preferir `===` (igualdad estricta).**

4.  **Contexto Lógico**: Todos los valores tienen un valor booleano asociado.
    *   **Valores *Falsy*:** `false`, `0`, `""`, `null`, `undefined`, `NaN`.
    *   **Valores *Truthy*:** Todo lo demás (incluyendo `[]`, `{}`, `"false"`).

5.  **Cortocircuitos (`&&` y `||`)**: No necesariamente devuelven booleanos; devuelven uno de los operandos.
    *   `a || b`: Si `a` es *truthy*, devuelve `a`; si no, devuelve `b`.
    *   `a && b`: Si `a` es *falsy*, devuelve `a`; si no, devuelve `b`.

6.  **Operador de Fusión Nula (`??`)**: Devuelve el operando derecho solo si el izquierdo es `null` o `undefined`. Es ideal para asignar valores por defecto sin verse afectado por otros valores *falsy* como `0` o `""`.

```javascript
const valor = 0 ?? 'default';  // 0 (porque 0 no es null/undefined)
const valor2 = 0 || 'default'; // 'default' (porque 0 es falsy)
```

### Ejemplos de Coerción "Curiosa"

```javascript
[] + []        // ""  (ambos se convierten a string vacío)
[] + {}        // "[object Object]"
{} + []        // 0 (si se interpreta como bloque + [])
true + true    // 2
'5' - 3        // 2
'5' + 3        // "53"
```

---

> [!TIP]
> ### Recomendaciones Finales
> 
> *   **Igualdad Estricta:** Usar siempre `===` y `!==` para evitar sorpresas por coerción.
> *   **Claridad:** Convertir explícitamente (`Number()`, `String()`) antes de operar si hay incertidumbre sobre el tipo.
> *   **Valores por Defecto:** Preferir `??` para valores por defecto cuando el `0` o las cadenas vacías `""` son valores válidos en tu lógica.

---

