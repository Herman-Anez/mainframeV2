# Estructuras de Control: Condicionales

## `if` / `else if` / `else`

Es la estructura fundamental para la toma de decisiones basada en condiciones lógicas.

```javascript
if (condicion) {
  // bloque si es verdadero
} else if (otraCondicion) {
  // bloque si la anterior es falsa y esta es verdadera
} else {
  // bloque si todas las anteriores son falsas
}
```

> [!NOTE]
> La **condición** se evalúa y se fuerza automáticamente a un valor booleano (*truthy* o *falsy*). Se pueden anidar sin límite técnico, pero un exceso de `else if` suele indicar la necesidad de un `switch` o un objeto de mapeo para mejorar la legibilidad.

---

## Operador Ternario

Es una forma concisa de devolver un valor basado en una condición. Es ideal para asignaciones directas.

```javascript
const acceso = edad >= 18 ? 'Permitido' : 'Denegado';
```

*   **Anidamiento:** Aunque es técnicamente posible anidarlos, se pierde legibilidad rápidamente. Se recomienda evitarlos en casos complejos.

---

## `switch`

Evalúa una expresión y compara su valor con diferentes casos utilizando **comparación estricta (`===`)**.

```javascript
switch (fruta) {
  case 'manzana':
    precio = 1;
    break;
  case 'pera':
  case 'uva':   // Casos agrupados: comparten el mismo bloque
    precio = 2;
    break;
  default:
    precio = 0;
}
```

*   **Fall-through:** Si se omite el `break`, la ejecución continúa en el siguiente bloque `case` hasta encontrar un `break` o llegar al final del `switch`.
*   **Default:** Es opcional y actúa como el bloque de escape si ninguna coincidencia ocurre.
*   **Flexibilidad:** Tanto la expresión del `switch` como los `case` pueden ser de cualquier tipo de dato.

---

## Condicionales de Cortocircuito

Aprovechan el comportamiento de los operadores `&&` y `||` para ejecutar código de forma condicional y compacta.

```javascript
// Equivale a: if (isLogged) mostrarDashboard();
isLogged && mostrarDashboard();

// Asigna 'opciones' si es truthy, de lo contrario asigna un objeto vacío
config = opciones || {};
```

---

> [!TIP]
> ### Patrones Recomendados
> 
> *   **Simplicidad:** Preferir `if` para condiciones binarias directas.
> *   **Legibilidad:** Usar `switch` cuando se manejan múltiples valores discretos para una misma variable.
> *   **Especificidad:** Evaluar condiciones de la más específica a la más general.
> *   **Early Return:** En funciones, es preferible usar retornos tempranos para evitar niveles profundos de anidamiento.

---


---
[back](../index)
