# Scope y Closures

El manejo del ámbito y las clausuras es fundamental para entender cómo JavaScript gestiona la memoria y el acceso a los datos.

---

## 1. Scope (Ámbito)

El ámbito determina la visibilidad y accesibilidad de las variables en diferentes partes del código.

### Tipos de Ámbito
*   **Ámbito Global:** Variables declaradas fuera de cualquier función o bloque. Son accesibles desde cualquier lugar y, en el navegador, se convierten en propiedades del objeto `window`.
*   **Ámbito de Función:** Cada función crea su propio contexto. Las variables declaradas con `var`, `let` o `const` dentro de una función son locales a ella.
*   **Ámbito de Bloque:** Introducido en ES6 con `let` y `const`. Estas variables están limitadas al bloque encerrado entre llaves `{}` (`if`, `for`, `while`, etc.).

### Scope Chain (Cadena de Ámbitos)
Cuando se intenta acceder a una variable, el motor de JavaScript la busca en el ámbito actual. Si no la encuentra, sube al ámbito superior inmediato, y así sucesivamente hasta llegar al ámbito global.

---

## 2. Closure (Clausura)

Un *closure* ocurre cuando una función "recuerda" y mantiene acceso a las variables de su ámbito léxico original, incluso después de que dicho ámbito haya finalizado su ejecución.

```javascript
function crearContador() {
  let cuenta = 0;
  return function() {
    cuenta++;
    return cuenta;
  };
}

const contador1 = crearContador();
console.log(contador1()); // Output: 1
console.log(contador1()); // Output: 2
```

> [!NOTE]
> En este ejemplo, la función interna mantiene viva la variable `cuenta`. Cada llamada a `crearContador()` genera un nuevo contexto con su propia instancia de `cuenta`.

---

## 3. Aplicaciones Prácticas

*   **Encapsulación:** Permite simular métodos o propiedades privadas (ocultación de datos).
*   **Fábricas de Funciones:** Creación de funciones configurables con un contexto específico.
*   **Manejo de Eventos:** Mantener el estado en funciones que se ejecutarán de forma asíncrona.
*   **Memoización:** Almacenar resultados de operaciones costosas en un caché privado.

### Ejemplo Clásico: Closures en Bucles
```javascript
// Problema con var (ámbito de función/global)
for (var i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 100);
}
// Imprime: 3, 3, 3

// Solución con let (ámbito de bloque)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Imprime: 0, 1, 2
```

---

## Consideraciones Finales

> [!IMPORTANT]
> **Referencia, no Copia:** Los *closures* capturan la referencia a la variable, no su valor en el momento de la creación. Si la variable cambia en el ámbito exterior antes de que el closure se ejecute, este verá el valor actualizado.

> [!TIP]
> **Rendimiento:** Debido a que mantienen referencias al ámbito exterior, los *closures* pueden impedir que el *Garbage Collector* libere memoria. Úsalos con sabiduría, pero no los evites; son una herramienta esencial del lenguaje.

---