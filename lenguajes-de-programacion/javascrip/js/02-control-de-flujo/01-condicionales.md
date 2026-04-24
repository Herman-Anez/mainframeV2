
02-control-de-flujo
---

## Archivo: `01-condicionales.md`

if / else if / else

La estructura básica de toma de decisiones.
```js
if (condición) {
  // bloque si verdadero
} else if (otraCondición) {
  // bloque si la anterior es falsa y esta es verdadera
} else {
  // bloque si todas las anteriores son falsas
}

    La condición se evalúa y se fuerza a booleano (truthy/falsy).
```

    Se pueden anidar sin límite, pero un exceso de else if se puede sustituir por switch o un objeto de mapeo.

### Operador ternario

Forma concisa de devolver un valor u otro según condición.
```js
const access = edad >= 18 ? 'Permitido' : 'Denegado';
```

    Se puede anidar, pero pierde legibilidad rápidamente; mejor evitarlo en casos complejos.

### Switch

Evalúa una expresión y compara su valor con cada caso usando comparación estricta (===).
```js
switch (fruta) {
  case 'manzana':
    precio = 1;
    break;
  case 'pera':
  case 'uva':   // ambos casos comparten el mismo bloque
    precio = 2;
    break;
  default:
    precio = 0;
}

    Fall-through: si no se coloca break, la ejecución continúa con el siguiente caso hasta encontrar un break o el final. A veces se usa a propósito (como en el ejemplo), pero debe documentarse.
```

    El default es opcional; se ejecuta si ningún caso coincide.

    La expresión del switch y los case pueden ser cualquier valor (no solo números o strings).

### Condicionales de cortocircuito

Uso de && y || para ejecutar código condicionalmente.
```js
isLogged && mostrarDashboard();  // equivale a if (isLogged) mostrarDashboard();
config = opciones || {};         // asigna opciones si es truthy, si no, {}
```

### Patrones recomendados

    Preferir if para condiciones binarias simples.

    Usar switch cuando hay múltiples valores discretos a comparar (más legible que muchos else if).

    Evaluar las condiciones de la más específica a la más general, o usar early returns en funciones.

---
