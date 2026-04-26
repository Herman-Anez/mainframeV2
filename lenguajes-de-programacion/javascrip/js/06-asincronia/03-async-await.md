## Archivo: `03-async-await.md`


async/await es azúcar sintáctico sobre las promesas, que permite escribir código asíncrono como si fuera síncrono, mejorando la legibilidad.
Función async

Una función precedida por async siempre devuelve una promesa. Si la función retorna un valor (no promesa), la promesa se resuelve con ese valor. Si lanza una excepción, la promesa se rechaza.
```js
async function obtenerDatos() {
  return 42;
}
obtenerDatos().then(console.log); // 42
```

### Palabra clave await

Solo se puede usar dentro de funciones async. Pausa la ejecución de la función hasta que la promesa se resuelva, y devuelve el valor resuelto.
```js
async function mostrarUsuario(id) {
  const response = await fetch(`/api/user/${id}`);
  const user = await response.json();
  console.log(user);
}
```

    Si la promesa se rechaza, await lanza una excepción, que se puede capturar con try/catch.

    No bloquea el hilo principal; el runtime puede atender otras tareas mientras espera.

### Manejo de errores con try/catch
```js
async function tarea() {
  try {
    const datos = await funcionQuePuedeFallar();
    return datos;
  } catch (error) {
    console.error('Falló:', error);
    // Podemos devolver valor por defecto o relanzar
    throw error;
  }
}
```

### Uso de await fuera de async (top-level await)

En módulos ES, el estándar permite await a nivel de cuerpo del módulo sin necesidad de función async (ES2022). Facilita la inicialización asíncrona de módulos.
Combinación con Promise.all

Como await detiene la ejecución secuencialmente, si necesitamos lanzar varias operaciones concurrentes debemos iniciar las promesas sin esperar y luego usar await Promise.all(...).
```js
async function cargarEnParalelo() {
  const [usr, posts] = await Promise.all([
    fetch('/user').then(r => r.json()),
    fetch('/posts').then(r => r.json())
  ]);
}
```

### Cuidado con bucles

    for...of funciona bien con await si se necesita secuencialidad.

    No usar forEach con await porque el callback de forEach no es async y no esperará realmente.

### Errores comunes

    Olvidar que async hace que la función siempre retorne una promesa, lo que puede cambiar la interfaz de la función.

    No manejar errores, dejando promesas rechazadas silenciosas (en Node las advertencias, en navegador eventos unhandledrejection).

    No aprovechar la concurrencia y usar await secuencial para tareas independientes.

---

---
[back](../index)
