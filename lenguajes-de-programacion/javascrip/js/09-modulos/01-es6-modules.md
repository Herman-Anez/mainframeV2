
## Archivo: `01-es6-modules.md`


Los módulos ES6 (ECMAScript 2015) son el sistema de módulos nativo de js. Permiten encapsular código, exportar e importar funcionalidades y cargar dependencias de forma declarativa.
Conceptos básicos

    Cada archivo .js que use import/export es un módulo.

    Los módulos se ejecutan en modo estricto automáticamente.

    El ámbito de un módulo es propio: las variables, funciones y clases definidas no se filtran al ámbito global a menos que se exporten y se importen expresamente.

    Los módulos se cargan de forma asíncrona y diferida (como <script type="module">), lo que evita bloqueos del HTML.

### Exportaciones

Se puede exportar cualquier declaración (variables, funciones, clases) o valores directamente.
Exportaciones nombradas (named exports)

Permiten exportar varias cosas desde un módulo.
```js
// matematicas.js
export const PI = 3.1416;
export function suma(a, b) { return a + b; }
export class Calculadora { /* ... */ }
```

También se puede exportar al final con una sola sentencia:
```js
const PI = 3.1416;
function suma(a, b) { return a + b; }
export { PI, suma };
```

Se pueden renombrar con as:
```js
export { suma as sumar };
```

### Exportación por defecto (default export)

Un módulo puede tener una única exportación por defecto. Se suele usar para exportar la entidad principal del módulo (una función, una clase, un objeto).
```js
// calculadora.js
export default class Calculadora {
  // ...
}
// o bien:
// export { Calculadora as default };
```

También se puede exportar una función anónima o un valor directamente:
```js
export default function() { /* ... */ }
```

No se debe abusar de las exportaciones por defecto; tienden a hacer menos explícita la importación.
Importaciones
Importación nombrada
```js
import { PI, suma, Calculadora } from './matematicas.js';

    Las rutas deben ser completas (incluyendo extensión) en muchos entornos (navegador, Deno). En Node con módulos ES se puede omitir .js si el empaquetador lo resuelve.
```

    Los nombres deben coincidir con los exportados, a menos que se use alias:

```js
import { suma as add } from './matematicas.js';
```

### Importación por defecto
```js
import Calculadora from './calculadora.js';
```

Puede tener cualquier nombre (no está ligado sintácticamente).
Importación combinada
```js
import React, { useState, useEffect } from 'react';
```

### Importación de todo el módulo (namespace)
```js
import * as Mat from './matematicas.js';
console.log(Mat.PI, Mat.suma(2,3));
```

Crea un objeto módulo con todas las exportaciones nombradas (no incluye la exportación por defecto, o la incluye como .default).
Importación solo para efectos secundarios
```js
import './estilos.css'; // ejecuta el módulo sin importar nada
```

Se usa para cargar CSS, polyfills o configurar librerías.
Ejecución de módulos

    Las importaciones son estáticas: el motor resuelve todas las dependencias en tiempo de compilación (no se puede usar import dentro de condicionales).

    Para importación dinámica existe la función import().

    Los módulos se evalúan solo la primera vez que se importan; las exportaciones son enlazadas (no copiadas): si el módulo exporta una variable y la modifica internamente, los importadores ven el nuevo valor (referencia viva, solo para exportaciones nombradas).

### import() dinámico

Devuelve una promesa del módulo completo. Permite cargar módulos bajo demanda (code splitting).
```js
const modulo = await import('./utilidades.js');
modulo.funcion();
```

Se puede usar en cualquier contexto, no solo en el nivel superior. Es común en SPA para lazy loading de rutas.
Compatibilidad en navegadores

Para usar módulos en un HTML:
```html
<script type="module" src="app.js"></script>
```

Los módulos se cargan con CORS, así que no funcionan desde file:// (necesitan un servidor). Se pueden usar importmap para controlar la resolución de módulos.
Tree shaking y agrupadores

Los bundlers (Webpack, Vite, Rollup) analizan las importaciones estáticas para eliminar código no usado (tree shaking). Por eso las exportaciones nombradas suelen facilitar este proceso.
Buenas prácticas

    Prefiere exportaciones nombradas para APIs claras.

    Usa default solo para componentes principales (un componente React, por ejemplo).

    Mantén los módulos pequeños y cohesivos.

    No mezcles lógica y efectos secundarios; los módulos con efectos secundarios dificultan el testing y el tree-shaking.

---
