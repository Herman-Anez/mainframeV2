# Async / Await en JavaScript

`async/await` es una mejora sintáctica (azúcar sintáctico) introducida en ES2017 sobre las promesas. Permite escribir código asíncrono con una estructura que se asemeja al código síncrono, lo que facilita enormemente su lectura y mantenimiento.

---

## La función `async`

Para utilizar `await`, primero debemos definir una función como `async`.

*   **Retorno automático:** Una función `async` siempre devuelve una promesa.
*   **Resolución:** Si la función retorna un valor que no es una promesa, JavaScript lo envuelve automáticamente en una promesa resuelta con ese valor.
*   **Rechazo:** Si la función lanza una excepción (`throw`), la promesa se rechaza con ese error.

```javascript
async function obtenerNumero() {
  return 42; // Equivalente a Promise.resolve(42)
}

obtenerNumero().then(console.log); // 42
```

---

## El operador `await`

La palabra clave `await` hace que la ejecución de la función `async` se pause hasta que la promesa se resuelva (ya sea exitosamente o con error).

```javascript
async function mostrarPerfil(id) {
  const respuesta = await fetch(`/api/usuarios/${id}`);
  const usuario = await respuesta.json();
  console.log(usuario.nombre);
}
```

> [!IMPORTANT]
> `await` solo puede ser utilizado dentro de funciones marcadas con `async` (con la excepción del **top-level await** en módulos ES). Aunque pausa la función, **no bloquea el hilo principal** del navegador, permitiendo que otras tareas continúen ejecutándose.

---

## Manejo de Errores con `try/catch`

A diferencia de las promesas donde se usa `.catch()`, con `async/await` utilizamos los bloques estándar de JavaScript para el manejo de excepciones.

```javascript
async function realizarTarea() {
  try {
    const datos = await servicioPropensoAFallar();
    return datos;
  } catch (error) {
    console.error('Se produjo un error en la tarea:', error.message);
    // Podemos relanzar el error o devolver un valor por defecto
    throw error;
  }
}
```

---

## Concurrencia y `Promise.all`

Uno de los errores más comunes es encadenar `await` de forma secuencial para tareas que podrían ejecutarse al mismo tiempo, lo que aumenta el tiempo total de espera.

```javascript
// FORMA INCORRECTA (Secuencial lenta)
const user = await fetchUser();
const posts = await fetchPosts();

// FORMA CORRECTA (Paralelo veloz)
const [user, posts] = await Promise.all([
  fetchUser(),
  fetchPosts()
]);
```

---

## Bucles y Operaciones Asíncronas

> [!WARNING]
> Ten mucho cuidado al usar `await` dentro de bucles:
> *   **`for...of` / `for`:** Funcionan correctamente y esperan a cada iteración (secuencial).
> *   **`forEach`:** **No funciona con await**. El callback de `forEach` se lanza y no espera a que termine antes de pasar al siguiente elemento. Usa `Promise.all` con `map` si quieres paralelismo o un bucle `for...of` si quieres secuencialidad.

---

## Errores Comunes y Buenas Prácticas

1.  **Olvidar el retorno de promesa:** Recordar que llamar a una función `async` devuelve una promesa, incluso si el código interno parece síncrono.
2.  **Top-level await:** En módulos ES modernos (ES2022+), puedes usar `await` directamente en el nivel superior del archivo sin envolverlo en una función `async`.
3.  **Falta de manejo de errores:** No envolver los `await` en `try/catch` puede llevar a errores silenciosos o cierres inesperados de la aplicación (especialmente en Node.js).

---
[Volver al Índice](../js-index.md)
