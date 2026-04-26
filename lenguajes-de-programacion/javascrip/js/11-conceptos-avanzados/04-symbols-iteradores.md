# Symbols e Iteradores

Los **Symbols** proporcionan una forma de crear claves de propiedad únicas, mientras que los **Iteradores** definen protocolos estandarizados para recorrer estructuras de datos.

---

## Symbol

Es un tipo de dato primitivo introducido en ES6. Cada símbolo es **único** e **inmutable**, incluso si tienen la misma descripción.

```js
const id = Symbol('id');
const user = { 
  [id]: 123, 
  nombre: 'Juan' 
};

console.log(user[id]); // 123
Object.keys(user);     // ['nombre'] (los símbolos son omitidos)
Object.getOwnPropertySymbols(user); // [Symbol(id)]
```

### Símbolos conocidos (*Well-known Symbols*)
Son propiedades estáticas del objeto `Symbol` que permiten personalizar comportamientos internos del lenguaje.

---

## El protocolo de Iteración

### `Symbol.iterator`

Define el iterador por defecto de un objeto. Es lo que permite que un objeto sea utilizado en un bucle `for...of`, con el operador *spread* `[...]`, o con `Array.from()`.

```js
const rango = {
  inicio: 1,
  fin: 5,
  [Symbol.iterator]() {
    let actual = this.inicio;
    const fin = this.fin;

    return {
      next() {
        if (actual <= fin) {
          return { value: actual++, done: false };
        }
        return { value: undefined, done: true };
      }
    };
  }
};

for (const n of rango) console.log(n); // 1 2 3 4 5
```

> [!TIP]
> Puedes simplificar la implementación de iteradores utilizando **generadores**:
> ```js
> *[Symbol.iterator]() {
>   for (let i = this.inicio; i <= this.fin; i++) yield i;
> }
> ```

---

## Iteración Asíncrona

### `Symbol.asyncIterator`

Define cómo debe comportarse un objeto al ser recorrido de forma asíncrona mediante `for await...of`.

```js
const paginador = {
  pagina: 1,
  async *[Symbol.asyncIterator]() {
    while (this.pagina <= 3) {
      const data = await fetch(`/api/datos?p=${this.pagina++}`).then(r => r.json());
      yield data;
    }
  }
};
```

---

## Otros Símbolos Importantes

- **`Symbol.toPrimitive`**: Controla cómo se convierte un objeto a un valor primitivo (según si se espera un número o un string).
- **`Symbol.toStringTag`**: Personaliza el string devuelto por `Object.prototype.toString.call(obj)`.
- **`Symbol.hasInstance`**: Permite personalizar el comportamiento del operador `instanceof`.
- **`Symbol.species`**: Permite a las clases derivadas indicar qué constructor deben usar los métodos que crean copias (como `map` o `filter`).

---

## Uso Práctico

1. **Evitar colisiones:** Usar símbolos para añadir metadatos a objetos sin riesgo de sobrescribir propiedades existentes o ser enumerados accidentalmente.
2. **Estructuras personalizadas:** Hacer que tus propias clases (listas, árboles, grafos) sean compatibles con la sintaxis nativa de iteración.
3. **Evaluación Perezosa (*Lazy evaluation*):** Crear iteradores que generen valores solo cuando se solicitan, ahorrando memoria en colecciones potencialmente infinitas o muy grandes.

> [!NOTE]
> Un objeto es **Iterable** si implementa `Symbol.iterator`. Un objeto es **Array-like** si tiene una propiedad `length` e índices numéricos, pero no necesariamente es iterable (ej: el objeto `arguments` antiguo).

---
[back](../index)
