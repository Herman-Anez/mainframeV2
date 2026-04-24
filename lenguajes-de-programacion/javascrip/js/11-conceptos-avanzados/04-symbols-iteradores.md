
## Archivo: `04-symbols-iteradores.md`

Symbol

Tipo de dato primitivo introducido en ES6. Cada símbolo es único e inmutable. Se crea con Symbol('descripcion'), donde la descripción es solo para depuración. Los símbolos pueden ser propiedades de objetos, evitando colisiones de nombres.
```js
const id = Symbol('id');
const user = { [id]: 123, nombre: 'Juan' };
console.log(user[id]); // 123
Object.keys(user); // ['nombre'] — no incluye símbolos
Object.getOwnPropertySymbols(user); // [Symbol(id)]
```

### Símbolos conocidos (Well-known Symbols)

Son propiedades estáticas de Symbol que representan protocolos internos del lenguaje. Permiten personalizar comportamientos de objetos.
Symbol.iterator

Define el iterador por defecto de un objeto. Se usa en for...of, spread, Array.from, etc.
```js
const rango = {
  inicio: 1,
  fin: 5,
  [Symbol.iterator]() {
    let actual = this.inicio;
    const fin = this.fin;
    return {
      next() {
        if (actual <= fin) return { value: actual++, done: false };
        return { value: undefined, done: true };
      }
    };
  }
};
for (const n of rango) console.log(n); // 1 2 3 4 5
```

También se puede implementar como generador:
```js
*[Symbol.iterator]() {
  for (let i = this.inicio; i <= this.fin; i++) yield i;
}
```

### Symbol.asyncIterator

Define el iterador asíncrono por defecto, usado en for await...of. Retorna un objeto con next() que devuelve Promise<{value, done}>.
```js
const paginador = {
  pagina: 1,
  async *[Symbol.asyncIterator]() {
    while (this.pagina <= 3) {
      yield await fetch(`/api/pagina/${this.pagina++}`).then(r => r.json());
    }
  }
};
```

### Otros well-known symbols

    Symbol.toPrimitive: controla la conversión a primitivo (hint: 'string' | 'number' | 'default').

    Symbol.toStringTag: define el resultado de Object.prototype.toString() (ej. [object MiClase]).

    Symbol.hasInstance: personaliza el comportamiento de instanceof.

    Symbol.species: usado por constructores para determinar qué clase usar al crear objetos derivados.

    Symbol.match, Symbol.replace, Symbol.search, Symbol.split: personalizan métodos de strings con expresiones regulares.

### Iteradores y objetos array-like

Implementar Symbol.iterator convierte un objeto en iterable. Para ser array-like además debe tener length y propiedades numéricas, pero no garantiza ser iterable.
Uso práctico

    Estructuras de datos personalizadas: listas enlazadas, árboles, que soporten for...of.

    Colecciones que cargan bajo demanda (lazy evaluation).

    Integración con spread y Array.from.

---
