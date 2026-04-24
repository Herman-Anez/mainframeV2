# Protocolo Iterable y Generadores

JavaScript proporciona protocolos estandarizados para la iteración, permitiendo que objetos personalizados se comporten como colecciones nativas.

---

## Protocolo Iterable

Un objeto se considera **iterable** si implementa el método `[Symbol.iterator]`. Este método debe devolver un **objeto iterador**.

### El Objeto Iterador
Un iterador es un objeto que contiene un método `next()`, el cual retorna un objeto con dos propiedades:
*   `value`: El valor actual de la iteración.
*   `done`: Un booleano que indica si la iteración ha finalizado (`true`) o no (`false`).

### Ejemplo de Implementación Manual
```javascript
const miIterable = {
  [Symbol.iterator]() {
    let i = 0;
    return {
      next() {
        i++;
        return { value: i, done: i > 3 };
      }
    };
  }
};

for (const valor of miIterable) { 
  console.log(valor); // Imprime: 1, 2, 3
}
```

> [!NOTE]
> Muchos objetos nativos ya son iterables por defecto: `Array`, `String`, `Map`, `Set`, `NodeList` y el objeto `arguments`. Los objetos literales (`{}`) **no** son iterables directamente.

---

## Consumo de Iterables

Existen múltiples constructores y operadores en JavaScript que "consumen" iterables de forma nativa:
*   **Bucles:** `for...of`
*   **Operador Spread:** `[...iterable]`
*   **Métodos de Array:** `Array.from(iterable)`
*   **Constructores:** `new Map(iterable)`, `new Set(iterable)`
*   **Promesas:** `Promise.all(iterable)`, `Promise.race(iterable)`, etc.

---

## Generadores (`function*`)

Los **Generadores** son funciones especiales que pueden pausar y reanudar su ejecución, produciendo una secuencia de valores bajo demanda. Son una forma extremadamente sencilla de crear iterables.

### Características Principales
*   Se declaran con el asterisco: `function* nombre()`.
*   Utilizan la palabra clave `yield` para devolver un valor y pausar la ejecución.
*   Llamar a la función no ejecuta su cuerpo, sino que devuelve un objeto iterador.

```javascript
function* contador(max) {
  let i = 0;
  while (i < max) {
    yield i++; // Pausa aquí y devuelve i
  }
  return 'Fin de la cuenta'; // Último valor con done: true
}

const gen = contador(3);
console.log(gen.next()); // { value: 0, done: false }
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 'Fin de la cuenta', done: true }
```

### Comunicación Bidireccional
Los generadores permiten recibir valores desde el exterior a través del método `next(valor)`. El valor pasado se convierte en el resultado de la expresión `yield` dentro del generador.

```javascript
function* conversacion() {
  const nombre = yield '¿Cómo te llamas?';
  yield `Mucho gusto, ${nombre}`;
}

const chat = conversacion();
console.log(chat.next().value);      // '¿Cómo te llamas?'
console.log(chat.next('Juan').value); // 'Mucho gusto, Juan'
```

---

## Generadores Asíncronos (`async function*`)

Combinan la potencia de los generadores con la asincronía (`async/await`). Devuelven un objeto que implementa el protocolo **async iterable**.

```javascript
async function* obtenerPaginas(urls) {
  for (const url of urls) {
    const respuesta = await fetch(url);
    yield await respuesta.json();
  }
}

// Se consumen mediante el bucle for await...of
for await (const datos of obtenerPaginas(listaDeUrls)) {
  console.log(datos);
}
```

> [!IMPORTANT]
> Los generadores asíncronos son ideales para manejar flujos de datos infinitos o muy grandes (streams) que llegan de forma asíncrona, como lecturas de archivos grandes o resultados paginados de una API.
