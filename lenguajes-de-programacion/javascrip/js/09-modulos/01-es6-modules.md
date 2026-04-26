# ES6 Modules (ESM)

Los **módulos ES6** (ECMAScript 2015) son el sistema de módulos nativo de JavaScript. Permiten encapsular código, exportar e importar funcionalidades y gestionar dependencias de forma declarativa y eficiente.

---

## Conceptos fundamentales

- **Ámbito propio:** Cada archivo `.js` que utiliza `import`/`export` es un módulo independiente. Las variables, funciones y clases definidas no se filtran al ámbito global a menos que se exporten explícitamente.
- **Modo estricto:** Los módulos se ejecutan en modo estricto (`'use strict'`) automáticamente.
- **Carga diferida:** Los módulos se cargan de forma asíncrona y diferida por defecto (equivalente a `<script type="module">`), evitando bloqueos en el renderizado del HTML.

---

## Exportaciones

Se puede exportar cualquier declaración (variables, funciones, clases) o valores literales de dos formas principales:

### 1. Exportaciones nombradas (*Named exports*)

Permiten exportar múltiples entidades desde un mismo módulo. Los nombres deben coincidir al importar.

```js
// matematicas.js
export const PI = 3.1416;

export function suma(a, b) { 
  return a + b; 
}

export class Calculadora { /* ... */ }
```

También se pueden exportar varias entidades al final del archivo:
```js
const PI = 3.1416;
function suma(a, b) { return a + b; }

export { PI, suma };
```

> [!TIP]
> Puedes renombrar exportaciones usando la palabra clave `as`:
> `export { suma as sumar };`

### 2. Exportación por defecto (*Default export*)

Un módulo puede tener una **única** exportación por defecto. Se utiliza generalmente para la entidad principal del archivo.

```js
// calculadora.js
export default class Calculadora {
  // ...
}

// También es posible:
// export { Calculadora as default };
```

> [!WARNING]
> No se recomienda abusar de las exportaciones por defecto, ya que pueden hacer que las importaciones sean menos explícitas y dificulten el mantenimiento en proyectos grandes.

---

## Importaciones

### Importación nombrada

```js
import { PI, suma, Calculadora } from './matematicas.js';
```

- **Rutas:** En navegadores y entornos como Deno, las rutas deben ser completas (incluyendo la extensión `.js`).
- **Alias:** Puedes renombrar importaciones para evitar colisiones de nombres:
  ```js
  import { suma as add } from './matematicas.js';
  ```

### Importación por defecto

```js
import MiCalculadora from './calculadora.js';
```
*Nota: Al ser una exportación por defecto, puedes asignarle cualquier nombre en el archivo de destino.*

### Importación combinada y Namespace

```js
// Combinada: default y nombradas
import React, { useState, useEffect } from 'react';

// Todo el módulo como un objeto (Namespace)
import * as Mat from './matematicas.js';
console.log(Mat.PI, Mat.suma(2, 3));
```

### Efectos secundarios

```js
import './estilos.css'; // Ejecuta el módulo sin importar ninguna variable específica
```
Se utiliza comúnmente para cargar CSS, polyfills o configuraciones globales.

---

## Ejecución y Carga Dinámica

- **Estática:** Las importaciones normales son estáticas; el motor de JS las resuelve antes de ejecutar el código. No pueden estar dentro de condicionales.
- **Referencias vivas:** Las exportaciones nombradas son enlaces en tiempo real. Si el módulo original modifica una variable exportada, el importador verá el cambio.

### `import()` dinámico

Permite cargar módulos bajo demanda, devolviendo una promesa. Es la base del *code splitting* y *lazy loading*.

```js
const modulo = await import('./utilidades.js');
modulo.funcion();
```

---

## Ámbito del Navegador

Para habilitar módulos en el navegador, se debe especificar el tipo en la etiqueta script:

```html
<script type="module" src="app.js"></script>
```

> [!IMPORTANT]
> Los módulos se cargan mediante CORS. Por seguridad, no funcionan a través del protocolo `file://`; requieren ser servidos mediante un servidor web (HTTP/HTTPS).

---

## Buenas prácticas

- **Claridad:** Prefiere exportaciones nombradas para APIs más descriptivas y seguras.
- **Tree-shaking:** Los empaquetadores (Webpack, Vite, Rollup) eliminan código no usado más fácilmente con exportaciones nombradas.
- **Cohesión:** Mantén los módulos pequeños, enfocados en una única responsabilidad.
- **Pureza:** Evita efectos secundarios en módulos lógicos; facilita el testing y la optimización.

---
[back](../index)
