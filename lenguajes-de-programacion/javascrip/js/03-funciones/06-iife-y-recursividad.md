# IIFE y Recursividad

Exploramos dos patrones avanzados de funciones: la ejecución inmediata para el aislamiento y la auto-llamada para la resolución de problemas complejos.

---

## 1. IIFE (Immediately Invoked Function Expression)

Una IIFE es una función que se define y se ejecuta en el mismo instante de su creación.

### Sintaxis Básica
```javascript
(function() {
  // Código aislado en un ámbito privado
})();

// Opcionalmente con parámetros
(function(nombre) {
  console.log(`Hola ${nombre}`);
})('Mundo');
```

### Características y Casos de Uso
*   **Ámbito Privado:** Evita la contaminación del ámbito global.
*   **Encapsulamiento:** Muy utilizado antes de ES6 para crear módulos.
*   **Patrón de Módulo Revelador:** Permite exponer solo lo necesario.

```javascript
const moduloContador = (function() {
  let privada = 0; // Variable inaccesible desde fuera
  return {
    incrementar() { privada++; },
    obtenerValor() { return privada; }
  };
})();

moduloContador.incrementar();
console.log(moduloContador.obtenerValor()); // Output: 1
```

---

## 2. Recursividad

La recursividad ocurre cuando una función se llama a sí misma para resolver una tarea, dividiéndola en instancias más pequeñas del mismo problema.

```javascript
function factorial(n) {
  if (n <= 1) return 1; // Caso Base
  return n * factorial(n - 1); // Llamada Recursiva
}
```

### Componentes Esenciales
1.  **Caso Base:** La condición que detiene la recursión. Sin ella, la función se llamaría infinitamente causando un *Stack Overflow*.
2.  **Llamada Recursiva:** La auto-llamada con argumentos que deben converger hacia el caso base.

---

## 3. Recursión de Cola (Tail Recursion)

Se produce cuando la llamada recursiva es la última operación que realiza la función. Algunos motores de JavaScript pueden optimizar esto mediante **TCO** (*Tail Call Optimization*) para no ocupar espacio adicional en la pila de ejecución.

```javascript
function factorialCola(n, acumulador = 1) {
  if (n <= 1) return acumulador;
  return factorialCola(n - 1, n * acumulador); // Llamada en posición de cola
}
```

---

## Precauciones y Aplicaciones

> [!WARNING]
> **Pila de Ejecución:** Cada llamada recursiva consume memoria en el *stack*. Si la profundidad es excesiva (miles de llamadas), se producirá un error de `Maximum call stack size exceeded`.

### Aplicaciones Comunes:
*   Recorridos de estructuras anidadas (JSON, Árboles DOM).
*   Algoritmos de ordenamiento y búsqueda (MergeSort, QuickSort).
*   Procesamiento de datos auto-similares (Fractales, Matemáticas).

---
