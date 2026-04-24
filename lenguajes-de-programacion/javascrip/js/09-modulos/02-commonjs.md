## Archivo: `02-commonjs.md`


CommonJS (CJS) es el sistema de módulos utilizado históricamente por Node.js (y otros entornos como Electron, Webpack, etc.). Es síncrono y está pensado para cargas en el servidor.
Exportar con module.exports y exports

En cada archivo CJS, las variables module, exports, require y __filename, __dirname están inyectadas.

    module.exports es el objeto (o valor) que realmente se exporta.

    exports es una referencia a module.exports; si se reasigna exports = {}, se rompe la referencia y no se exporta nada. Para exportar varias cosas, se asignan propiedades: exports.foo = ... o se usa directamente module.exports.

```js
// matematicas.cjs
function suma(a, b) { return a + b; }
const PI = 3.1416;
module.exports = { suma, PI };
```

También se puede exportar una sola función:
```js
// calculadora.cjs
class Calculadora {}
module.exports = Calculadora;
```

### Importar con require()
```js
const mate = require('./matematicas.cjs');
console.log(mate.suma(2,3));

    require es una función síncrona que devuelve el valor de module.exports del módulo requerido.
```

    El módulo se evalúa y cachea: una misma referencia devuelta en subsecuentes require.

    Las extensiones .js, .json y .node se resuelven automáticamente.

    Se pueden requerir directorios con un archivo index.js dentro.

### Carga cíclica

CommonJS maneja dependencias circulares devolviendo el objeto module.exports en el estado que tenga hasta ese momento (parcialmente cargado). Esto puede causar comportamientos inesperados; es mejor evitar ciclos.
Diferencias con ES Modules
Característica	CJS	ESM
Carga	Síncrona	Asíncrona (estática) / Dinámica con import()
Sintaxis	require / module.exports	import / export
Resolución en Node	Extensiones automáticas	Debe especificar extensión (si no se usa paquete)
Modo estricto	No por defecto	Sí, automático
Tree shaking	Difícil	Soportado nativamente
this en top-level	apunta a exports	undefined
Temporalidad	En tiempo de ejecución	Estática (salvo dinámica)
Interoperabilidad

Node.js permite importar módulos CJS desde ESM usando:
```js
import mod from 'modulo-cjs'; // toma el default export de CJS
import { nombrado } from 'modulo-cjs'; // falla si no se ha exportado nombrado explícitamente
```

Para importar ESM desde CJS se puede usar import() dinámica (asíncrono). No se puede usar require para módulos ESM.
¿Cuándo usar cada uno?

    Nuevos proyectos en Node: preferir ESM ("type": "module" en package.json).

    Proyectos legacy: CJS. Muchos paquetes npm aún distribuyen CJS.

    Bibliotecas: conviene publicar dual CJS/ESM para máxima compatibilidad.

### 10-apis-web
---
