# Parámetros y Operador Spread

JavaScript ofrece herramientas potentes para manejar los argumentos de las funciones de forma flexible y legible.

---

## 1. Parámetros por Defecto

Permiten asignar un valor predeterminado a un parámetro si el argumento enviado es `undefined`.

```javascript
function saludar(nombre = 'invitado') {
  return `Hola, ${nombre}`;
}

saludar();          // Output: Hola, invitado
saludar(undefined); // Output: Hola, invitado
saludar(null);      // Output: Hola, null (null se considera un valor definido)
```

> [!TIP]
> Las expresiones de los valores por defecto se evalúan en cada llamada (tiempo de ejecución) y pueden referenciar parámetros definidos anteriormente.

```javascript
function suma(a, b = a * 2) {
  return a + b;
}
suma(3); // Output: 9 (b toma el valor 3 * 2 = 6)
```

---

## 2. Parámetros Rest (`...`)

El parámetro *rest* permite representar un número indefinido de argumentos como un array real.

```javascript
function concatenar(separador, ...palabras) {
  return palabras.join(separador);
}

concatenar('-', 'a', 'b', 'c'); // Output: 'a-b-c'
```

### Reglas de Uso
*   **Posición Única:** Solo puede haber un parámetro *rest* por función.
*   **Posición Final:** Debe ser siempre el último parámetro en la lista.
*   **Superioridad sobre `arguments`:** Sustituye al objeto `arguments` de forma más clara, proporcionando un array con todos sus métodos (map, filter, etc.).
*   **En Arrow Functions:** Es la única forma de capturar múltiples argumentos dinámicos.

---

## 3. Operador Spread en Funciones

El operador `...` (*spread*) permite expandir un array u otro iterable en argumentos individuales durante la invocación de una función.

```javascript
const numeros = [5, 10, 15];
console.log(Math.max(...numeros)); // Equivalente a Math.max(5, 10, 15)

const fechaValores = [2025, 4, 12];
const fecha = new Date(...fechaValores); // Output: 12 de mayo de 2025
```

---

## 4. El Objeto `arguments`

Es un objeto similar a un array (pero no es un array real) disponible solo en funciones clásicas (no flecha).

```javascript
function mostrarArgumentos() {
  console.log(arguments[0]); // Acceso por índice
  console.log(arguments.length); // Cantidad de argumentos
}

mostrarArgumentos(1, 2, 3);
```

> [!IMPORTANT]
> Para usar métodos de array con `arguments`, debes convertirlo primero:
> `const argsArray = Array.from(arguments);` o `const argsArray = [...arguments];`.

---

## Buenas Prácticas

> [!NOTE]
> 1.  **Prioriza Parámetros Rest:** Son más legibles, seguros y proporcionan métodos de array nativos.
> 2.  **Usa Valores por Defecto:** Evita comprobaciones manuales de `undefined` dentro del cuerpo de la función.
> 3.  **Aprovecha el Spread:** Simplifica drásticamente la invocación de funciones que reciben múltiples argumentos a partir de colecciones de datos.

---

---
[back](../index)
