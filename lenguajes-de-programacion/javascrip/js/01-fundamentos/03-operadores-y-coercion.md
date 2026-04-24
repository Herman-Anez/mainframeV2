

## Archivo: `03-operadores-y-coercion.md`

Operadores más importantes
Categoría	Operadores
Aritméticos	+, -, *, /, %, ** (exponenciación)
Asignación	=, +=, -=, etc.
Comparación	==, !=, ===, !==, >, <, >=, <=
Lógicos	&&, ||, ?? (nullish coalescing)
Ternario	condición ? valorVerdadero : valorFalso
Unarios	!, ++, --, typeof, void
Relacionales	in, instanceof
Coerción de tipos

La coerción es la conversión automática o manual de un tipo a otro.
Coerción explícita (recomendada)

### String(valor)

### Number(valor), parseInt(), parseFloat()

### Boolean(valor)

### BigInt(valor)

### Symbol(valor)

### Coerción implícita

Muchos operadores fuerzan la conversión. Reglas básicas:

    Suma +:

        Si algún operando es string, el otro se convierte a string y se concatenan.

        En otro caso, ambos se convierten a number (si es posible) y se suman.

        null se convierte a 0, undefined a NaN en contexto numérico.

    Resta -, multiplicación *, división /, etc.: Ambos operandos se convierten a número.

    Comparación débil ==:

        Compara sin verificar tipo. Aplica un algoritmo complejo de coerción.

        Si los tipos son distintos, se fuerza la conversión de uno o ambos lados a número, string o booleano.

        Evitarla siempre que sea posible; usar === (igualdad estricta).

    Booleanos en contexto lógico: Todos los valores tienen un valor verdadero/falso asociado. Valores falsy: false, 0, "", null, undefined, NaN. Todo lo demás es truthy (incluyendo [], {}, "false").

    Operador lógico && y ||: No necesariamente devuelven booleanos; devuelven uno de los operandos.

        a || b: si a es truthy, devuelve a; si no, devuelve b.

        a && b: si a es falsy, devuelve a; si no, devuelve b.

    Operador de fusión nula ??: Devuelve el operando derecho solo si el izquierdo es null o undefined (no por falsy general). Ideal para valores por defecto.
```js
    const valor = 0 ?? 'default'; // 0 (porque 0 no es null/undefined)
    const valor2 = 0 || 'default'; // 'default' (porque 0 es falsy)
```

### Ejemplo de trampas con coerción
```js
[] + []        // ""  (ambos se convierten a string vacío)
[] + {}        // "[object Object]"
{} + []        // 0 (si se interpreta como bloque + [])
true + true    // 2
'5' - 3        // 2
'5' + 3        // "53"
```

### Recomendaciones

    Usar siempre === y !==.

    Convertir explícitamente antes de operar si hay incertidumbre.

    Preferir ?? para valores por defecto cuando 0 o "" son válidos.

---
