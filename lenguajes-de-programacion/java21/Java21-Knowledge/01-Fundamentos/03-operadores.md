# OPERADORES
3.1. Operadores aritméticos

+, -, *, /, % (módulo). Funcionan sobre tipos numéricos. División entera trunca. Precedencia: *, /, % antes que +, -.
3.2. Operadores unarios

### + (positivo), - (negación)

    ++ (incremento), -- (decremento), prefijo y sufijo.

### ! (negación lógica), ~ (complemento bit a bit)

3.3. Operadores relacionales y de igualdad

<, <=, >, >=, ==, !=. Devuelven boolean.

    == en tipos referencia compara identidad de objeto (direcciones), no contenido. Para igualdad de contenido se usa equals().

    Cuidado con autoboxing: Integer a = 200; Integer b = 200; a == b puede ser falso por el cache (el pool de enteros solo cubre -128 a 127).

3.4. Operadores lógicos

    Cortocircuito: && (AND), || (OR) – solo evalúan el segundo operando si es necesario.

    No cortocircuito: &, | (evalúan ambos operandos, también usados a nivel bit).

    ^ (XOR lógico o bit a bit según el contexto).

3.5. Operadores a nivel de bits

&, |, ^, ~, << (desplazamiento izquierda), >> (desplazamiento derecha con signo), >>> (desplazamiento derecha sin signo).
3.6. Operador de asignación y combinados

=, +=, -=, *=, /=, %=, &=, |=, ^=, <<=, >>=, >>>=.
```java
int x = 10;
x += 5;  // x = x + 5
```

3.7. Operador ternario

### condicion ? valorSiVerdadero : valorSiFalso
```java
String estado = (edad >= 18) ? "Adulto" : "Menor";
```

3.8. Operador instanceof y Pattern Matching

instanceof comprueba si un objeto es instancia de una clase/interface.
Desde Java 16 (estable), se puede realizar pattern matching para vincular una variable directamente:
```java
if (objeto instanceof String s) {
    System.out.println(s.toUpperCase());
}
```

La variable de patrón s existe únicamente si la comprobación es true. Además, se puede combinar con condiciones adicionales usando &&:
```java
if (objeto instanceof String s && s.length() > 5) { ... }
```

3.9. Operador de referencia a método ::

Permite referenciar métodos como lambdas: System.out::println, String::length, MiClase::new.
3.10. Operador -> (flecha)

Usado en lambdas y en switch expressions (que veremos en control de flujo). En lambdas: (a, b) -> a + b.
3.11. Precedencia de operadores

La tabla de precedencia ordena la evaluación. Lo más relevante:

### Postfijos (++ --)

### Unarios (+ - ! ~ ++ -- prefijos)

### Multiplicativos (* / %)

### Aditivos (+ -)

### Desplazamiento (<< >> >>>)

### Relacionales (< > <= >= instanceof)

### Igualdad (== !=)

### AND bit a bit (&)

### XOR bit a bit (^)

### OR bit a bit (|)

### AND lógico (&&)

### OR lógico (||)

### Ternario (?:)

### Asignación (= += ...)

Ante la duda, usar paréntesis.
