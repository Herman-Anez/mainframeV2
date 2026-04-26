# Funciones de Orden Superior

Una función de orden superior (*Higher-Order Function*) es un concepto fundamental de la programación funcional que permite tratar a las funciones como valores de primera clase.

---

## Definición

Una función se considera de orden superior si cumple al menos una de estas condiciones:
1.  **Recibe una función** como argumento (callback).
2.  **Retorna una función** como resultado.

---

## 1. Funciones que Reciben Callbacks

Los *callbacks* son funciones pasadas como argumentos para ser ejecutadas en un momento posterior o bajo ciertas condiciones.

### Ejemplos en el Lenguaje:
*   **Métodos de Array:** `map`, `filter`, `reduce`, `forEach`, `find`.
*   **Temporizadores:** `setTimeout`, `setInterval`.
*   **Eventos:** `addEventListener`.

```javascript
const numeros = [1, 2, 3];
const dobles = numeros.map(n => n * 2); // map es una función de orden superior
```

---

## 2. Funciones que Retornan Funciones

Esta técnica permite la creación de funciones personalizadas y la reutilización de lógica mediante configuraciones previas.

```javascript
function multiplicarPor(factor) {
  return function(numero) {
    return numero * factor;
  };
}

const duplicar = multiplicarPor(2);
console.log(duplicar(5)); // Output: 10
```

---

## 3. Métodos Funcionales de Array

Son los ejemplos más comunes de funciones de orden superior en el día a día:

| Método | Propósito |
| :--- | :--- |
| `map(fn)` | Transforma cada elemento y devuelve un nuevo array. |
| `filter(fn)` | Selecciona elementos que cumplen una condición (predicado). |
| `reduce(fn, init)` | Acumula todos los elementos en un único valor final. |
| `forEach(fn)` | Ejecuta una función para cada elemento (efectos secundarios). |
| `some(fn)` / `every(fn)` | Realiza comprobaciones lógicas sobre los elementos. |
| `find(fn)` | Retorna el primer elemento que cumpla la condición. |

> [!NOTE]
> Todos estos métodos reciben una función con la firma: `(elemento, indice, array)`.

---

## 4. Composición de Funciones

Permite combinar múltiples funciones para crear flujos de procesamiento complejos (*pipelines*).

```javascript
const compose = (f, g) => x => f(g(x));
const añadirExclamación = s => s + '!';
const gritar = s => s.toUpperCase();

const emocionar = compose(añadirExclamación, gritar);
console.log(emocionar('hola')); // Output: 'HOLA!'
```

---

## Beneficios y Recomendaciones

> [!TIP]
> *   **Abstracción:** Separan la lógica de iteración de la lógica de negocio.
> *   **Declaratividad:** El código describe el "qué" se quiere lograr, no el "cómo" iterar paso a paso.
> *   **Funciones Puras:** Prefiere usar funciones puras (sin efectos secundarios) como *callbacks* para asegurar que el código sea predecible y fácil de testear.

---
---
[back](../index)
