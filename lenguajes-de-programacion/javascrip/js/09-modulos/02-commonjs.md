# CommonJS (CJS)

**CommonJS** es el sistema de módulos utilizado históricamente por Node.js y otros entornos como Electron o Webpack (para compatibilidad). Está diseñado para una carga síncrona, ideal para entornos de servidor.

---

## Exportar módulos

En cada archivo CommonJS, se inyectan variables globales como `module`, `exports`, `require`, `__filename` y `__dirname`.

- **`module.exports`**: Es el objeto o valor que realmente se exporta al mundo exterior.
- **`exports`**: Es una referencia inicial a `module.exports`. 

```js
// matematicas.cjs
function suma(a, b) { return a + b; }
const PI = 3.1416;

module.exports = { suma, PI };
```

También se puede exportar una única entidad directamente:
```js
// calculadora.cjs
class Calculadora {}
module.exports = Calculadora;
```

> [!WARNING]
> Si reasignas `exports` directamente (ej: `exports = {}`), rompes la referencia a `module.exports` y no se exportará nada. Para exportar múltiples propiedades, usa `exports.propiedad = ...` o `module.exports = { ... }`.

---

## Importar con `require()`

```js
const mate = require('./matematicas.cjs');
console.log(mate.suma(2, 3));
```

- **Sincronía:** `require` es una función síncrona que bloquea la ejecución hasta que el módulo es cargado y evaluado.
- **Caché:** Los módulos se evalúan solo una vez. Los `require` subsecuentes devuelven la referencia cacheada.
- **Resolución:** Node.js resuelve automáticamente extensiones `.js`, `.json` y `.node`. También busca archivos `index.js` dentro de directorios.

---

## Diferencias con ES Modules

| Característica | CommonJS (CJS) | ES Modules (ESM) |
| :--- | :--- | :--- |
| **Carga** | Síncrona | Asíncrona (Estática / Dinámica) |
| **Sintaxis** | `require` / `module.exports` | `import` / `export` |
| **Resolución** | Extensiones automáticas | Especificación obligatoria de extensión |
| **Modo Estricto** | Opcional | Automático y obligatorio |
| **Tree shaking** | Muy difícil de optimizar | Soportado nativamente |
| **`this` (top-level)** | Apunta a `exports` | `undefined` |

---

## Interoperabilidad

Node.js permite la convivencia de ambos sistemas, con algunas reglas:

1. **Importar CJS desde ESM:**
   ```js
   import mod from './modulo.cjs'; // Toma el module.exports como default
   ```
2. **Importar ESM desde CJS:**
   Solo se puede hacer mediante el `import()` dinámico (asíncrono). `require` **no puede** cargar módulos ESM.

---

## Buenas prácticas

- **Modernización:** Prefiere ESM para nuevos proyectos (`"type": "module"` en `package.json`).
- **Librerías:** Considera publicar en formato dual (CJS y ESM) para máxima compatibilidad.
- **Ciclos:** Evita las dependencias circulares; aunque CJS las maneja devolviendo objetos parcialmente cargados, suelen causar errores lógicos difíciles de depurar.

---
[back](../index)
