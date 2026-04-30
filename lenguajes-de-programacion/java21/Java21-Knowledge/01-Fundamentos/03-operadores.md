# Operadores

Los operadores en Java permiten manipular datos, realizar cálculos matemáticos, comparaciones lógicas y operaciones a nivel de bits.

---

## Operadores aritméticos

Se utilizan para realizar operaciones matemáticas básicas sobre tipos numéricos.

| Operador | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `+` | Suma | `a + b` |
| `-` | Resta | `a - b` |
| `*` | Multiplicación | `a * b` |
| `/` | División | `a / b` |
| `%` | Módulo (resto) | `a % b` |

> [!WARNING]
> **División entera:** En Java, la división entre dos enteros trunca el resultado (ej: `5 / 2` es `2`). Para obtener decimales, al menos uno de los operandos debe ser de punto flotante.

---

## Operadores unarios

Requieren un solo operando y realizan tareas diversas como incrementar valores o negar expresiones.

- **`+` (positivo)** y **`-` (negación)** numérica.
- **`++` (incremento)** y **`--` (decremento)**: Pueden usarse como prefijo (`++x`) o sufijo (`x++`).
- **`!` (negación lógica)**: Invierte el valor de un booleano.
- **`~` (complemento bit a bit)**: Invierte los bits de un operando.

---

## Operadores relacionales y de igualdad

Comparan dos valores y devuelven un resultado de tipo `boolean`.

- `<`, `<=`, `>`, `>=`: Menor, menor o igual, mayor, mayor o igual.
- `==`, `!=`: Igualdad y desigualdad.

> [!IMPORTANT]
> **Comparación de objetos:** El operador `==` compara la **identidad** (dirección de memoria) en tipos de referencia. Para comparar el **contenido**, se debe usar el método `.equals()`.

> [!CAUTION]
> **Autoboxing e Integer Cache:** La comparación `Integer a = 200; Integer b = 200; a == b` puede devolver `false` porque el pool de enteros de la JVM solo cubre el rango de `-128` a `127`.

---

## Operadores lógicos

Se utilizan para combinar múltiples expresiones booleanas.

- **`&&` (AND)** y **`||` (OR)**: Operadores de **cortocircuito**. Solo evalúan el segundo operando si es necesario.
- **`&`**, **`|`**: Operadores lógicos que **siempre** evalúan ambos operandos (también usados a nivel de bits).
- **`^`**: XOR lógico o bit a bit según el contexto.

---

## Operadores a nivel de bits

Realizan operaciones directamente sobre la representación binaria de los datos.

- `&` (AND), `|` (OR), `^` (XOR), `~` (NOT).
- `<<`: Desplazamiento a la izquierda.
- `>>`: Desplazamiento a la derecha con signo.
- `>>>`: Desplazamiento a la derecha sin signo.

---

## Operadores de asignación y combinados

- **Simple**: `=`.
- **Compuestos**: `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`, `>>>=`.

```java
int x = 10;
x += 5;  // Equivalente a x = x + 5
```

---

## Operador ternario

Es una forma compacta de representar una estructura `if-else` que devuelve un valor.

**Sintaxis:** `condicion ? valorSiVerdadero : valorSiFalso`

```java
String estado = (edad >= 18) ? "Adulto" : "Menor";
```

---

## Operador `instanceof` y Pattern Matching

Comprueba si un objeto es instancia de una clase o interfaz específica.

### Pattern Matching (Java 16+)
Permite realizar la comprobación y la vinculación de una variable en un solo paso:

```java
if (objeto instanceof String s) {
    System.out.println(s.toUpperCase()); // 's' ya está casteada a String
}
```

> [!NOTE]
> La variable de patrón `s` existe únicamente si la comprobación es `true`. Se puede combinar con condiciones adicionales usando `&&`.

---

## Operadores modernos

- **Referencia a método (`::`)**: Permite referenciar métodos como lambdas (ej: `System.out::println`, `String::length`, `MiClase::new`).
- **Flecha (`->`)**: Usado en lambdas y en `switch expressions`. En lambdas: `(a, b) -> a + b`.

---

## Precedencia de operadores

La tabla de precedencia ordena la evaluación de mayor a menor prioridad:

1. **Postfijos**: `++`, `--`
2. **Unarios**: `+`, `-`, `!`, `~`, `++`, `--` (prefijos)
3. **Multiplicativos**: `*`, `/`, `%`
4. **Aditivos**: `+`, `-`
5. **Desplazamiento**: `<<`, `>>`, `>>>`
6. **Relacionales**: `<`, `>`, `<=`, `>=`, `instanceof`
7. **Igualdad**: `==`, `!=`
8. **Operadores Bit a Bit**: `&`, `^`, `|`
9. **Lógicos**: `&&`, `||`
10. **Ternario**: `?:`
11. **Asignación**: `=`, `+=`, `-=`, etc.

> [!TIP]
> Ante la duda sobre el orden de evaluación, el uso de **paréntesis** garantiza la claridad y el comportamiento deseado del código.
