
## Archivo: `02-bucles.md`

Bucle for clásico
```js
for (inicialización; condición; expresión final) {
  // cuerpo
}

    Se puede omitir cualquiera de las tres partes (por ejemplo, for(;;) es un bucle infinito).

    Todas las variables declaradas con var comparten ámbito; con let se crea un nuevo enlace en cada iteración (muy útil con closures).

while y do...while

    while: evalúa la condición antes de cada iteración. Puede no ejecutarse nunca.

    do...while: ejecuta el cuerpo al menos una vez y luego evalúa la condición.
```

js

### while (hayDatos()) { procesar(); }
do { intentar(); } while (reintentar);

### for...in

Recorre las claves enumerables de un objeto (incluyendo las heredadas a través de la cadena de prototipos).
```js
for (const key in objeto) {
  if (Object.hasOwn(objeto, key)) {
    console.log(key, objeto[key]);
  }
}

    No usar para arrays (recorre índices como strings y puede incluir propiedades añadidas).
```

    El orden no está garantizado para propiedades no numéricas.

    Para evitar propiedades heredadas, filtrar con Object.hasOwn() (o Object.prototype.hasOwnProperty.call()).

### for...of

Introducido en ES6, recorre los valores de un objeto iterable (arrays, strings, mapas, sets, generadores, NodeList, etc.).
```js
for (const valor of iterable) {
  console.log(valor);
}
```

    No funciona sobre objetos planos a menos que implementen Symbol.iterator.

    Sí respeta el orden natural del iterable.

    Muy útil para arrays cuando no se necesita el índice.

    Se puede combinar con entries(): for (const [i, v] of arr.entries()).

### Control de flujo dentro de bucles: break y continue

    break: termina inmediatamente el bucle.

    continue: salta a la siguiente iteración.

    Ambos afectan al bucle más cercano. Se pueden usar etiquetas (label:) para saltar de un bucle anidado exterior.

```js
exterior: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (i === j) continue exterior; // salta a la siguiente iteración de 'i'
    console.log(i, j);
  }
}
```

### Buenas prácticas

    Preferir for...of (o métodos funcionales como .forEach, .map) para arrays sobre el for clásico.

    No usar for...in en arrays; para objetos, considerar Object.keys()/Object.values()/Object.entries() con for...of.

    Cuidado con modificar la longitud de un array mientras se itera con un for clásico.

---
