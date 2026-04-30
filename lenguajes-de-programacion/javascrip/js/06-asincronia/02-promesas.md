# Promesas en JavaScript

Una `Promise` (promesa) es un objeto que representa la eventual finalización (o falla) de una operación asíncrona y su valor resultante. Permite manejar operaciones asíncronas de una forma más limpia que los callbacks tradicionales.

---

## Estados de una Promesa

Una promesa puede encontrarse en uno de estos tres estados:

1.  **Pending (Pendiente):** Estado inicial, la operación no ha terminado ni ha fallado.
2.  **Fulfilled (Cumplida):** La operación se completó con éxito y devuelve un valor.
3.  **Rejected (Rechazada):** La operación falló y devuelve un motivo (generalmente un objeto `Error`).

> [!IMPORTANT]
> Una vez que una promesa cambia a `fulfilled` o `rejected`, su estado se vuelve inmutable (se dice que la promesa está **settled** o establecida).

---

## Creación de una Promesa

Se utiliza el constructor `new Promise`, el cual recibe una función ejecutora con dos argumentos: `resolve` y `reject`.

```javascript
const miPromesa = new Promise((resolve, reject) => {
  const exito = true;
  
  // Simulando operación asíncrona
  setTimeout(() => {
    if (exito) {
      resolve('¡Operación exitosa!');
    } else {
      reject(new Error('Algo salió mal'));
    }
  }, 1000);
});
```

---

## Consumo de Promesas

Para interactuar con el resultado de una promesa, se utilizan los siguientes métodos:

*   **`.then(onFulfilled, onRejected)`:** Programa callbacks para cuando la promesa se resuelva o se rechace. Retorna una nueva promesa, lo que permite el encadenamiento.
*   **`.catch(onRejected)`:** Es un atajo para `.then(null, onRejected)`. Se encarga exclusivamente del manejo de errores.
*   **`.finally(onFinally)`:** Se ejecuta siempre al terminar la promesa, independientemente de si fue exitosa o fallida. No recibe argumentos y no altera el resultado de la promesa.

```javascript
fetch('/api/usuario')
  .then(response => response.json())
  .then(data => console.log('Datos:', data))
  .catch(error => console.error('Error:', error))
  .finally(() => console.log('Proceso finalizado'));
```

---

## Métodos Estáticos y Utilidades

JavaScript ofrece métodos para gestionar múltiples promesas simultáneamente:

| Método | Descripción |
| :--- | :--- |
| `Promise.all(iterable)` | Espera a que **todas** se cumplan. Si una falla, rechaza inmediatamente. |
| `Promise.allSettled(iterable)` | Espera a que todas terminen, sin importar si fallan o no. |
| `Promise.race(iterable)` | Se resuelve o rechaza con el resultado de la **primera** que termine. |
| `Promise.any(iterable)` | Se resuelve con la primera que se **cumpla**. Si todas fallan, devuelve un `AggregateError`. |

> [!TIP]
> Usa `Promise.resolve(valor)` o `Promise.reject(razon)` para crear promesas ya establecidas instantáneamente, útil para normalizar APIs o iniciar cadenas de promesas.

---

## Manejo de Errores y Microtareas

### Propagación de Errores
Cualquier error lanzado dentro de un `.then` o en el ejecutor de la promesa se convierte automáticamente en un rechazo. Siempre es una buena práctica terminar las cadenas de promesas con un `.catch()` para evitar advertencias de "Uncaught Promise Rejection".

### Microtareas (Microtasks)
Los callbacks de las promesas no se ejecutan inmediatamente. Se añaden a la **Cola de Microtareas**, que tiene prioridad sobre la cola de tareas (macrotareas como `setTimeout`).

> [!NOTE]
> El motor de JavaScript procesará todas las microtareas acumuladas antes de ceder el control al navegador para renderizar o ejecutar la siguiente macrotarea.

---
[Volver al Índice](../js-index.md)
