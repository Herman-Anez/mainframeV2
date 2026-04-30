# Fetch API en JavaScript

`fetch` es la interfaz moderna de JavaScript para realizar peticiones HTTP de forma asíncrona. Está integrada en el navegador y disponible de forma nativa en Node.js (versión 18+), reemplazando al antiguo `XMLHttpRequest`.

---

## Sintaxis y Uso Básico

La función `fetch()` recibe una URL y un objeto opcional de configuración, devolviendo una **Promesa** que resuelve en un objeto `Response`.

```javascript
fetch('https://api.ejemplo.com/datos')
  .then(response => {
    // Es vital verificar si la respuesta es exitosa (status 200-299)
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }
    return response.json(); // Retorna otra promesa con los datos parseados
  })
  .then(data => console.log('Datos recibidos:', data))
  .catch(error => console.error('Error en la petición:', error));
```

---

## El Objeto `Response`

Representa la respuesta a la petición. Contiene metadatos y métodos para consumir el cuerpo del mensaje.

### Propiedades Clave
*   **`response.ok`**: Booleano que indica si el código de estado está entre 200 y 299.
*   **`response.status`**: Código de estado HTTP (ej. 200, 404, 500).
*   **`response.headers`**: Objeto que contiene las cabeceras de la respuesta.
*   **`response.url`**: La URL final de la respuesta (útil tras redirecciones).

### Métodos para Consumir el Cuerpo (Body)
> [!IMPORTANT]
> El cuerpo de la respuesta es un flujo (stream) que solo puede ser consumido **una vez**.

| Método | Resultado esperado |
| :--- | :--- |
| `response.json()` | Parsea el contenido como JSON y devuelve un objeto/array. |
| `response.text()` | Devuelve el contenido como una cadena de texto plano. |
| `response.blob()` | Devuelve un objeto Blob (útil para imágenes o archivos). |
| `response.formData()` | Parsea el contenido como datos de formulario. |
| `response.arrayBuffer()`| Devuelve el contenido como un buffer binario puro. |

---

## Configuración de la Petición

Para realizar peticiones distintas a `GET` (como `POST`, `PUT`, `DELETE`), pasamos un objeto de opciones como segundo argumento.

```javascript
fetch('/api/productos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer tu_token_aqui'
  },
  body: JSON.stringify({ nombre: 'Nuevo Producto', precio: 25.50 })
});
```

---

## Manejo de Errores

> [!WARNING]
> **Error común:** `fetch` **no se rechaza** en errores HTTP como 404 o 500. La promesa solo se rechaza si ocurre un fallo de red (ej. falta de conexión o DNS fallido). Por ello, siempre debes validar `response.ok` o `response.status` manualmente.

---

## Cancelación con `AbortController`

Puedes cancelar una petición en curso (por ejemplo, si el usuario cambia de página o para implementar un *timeout*).

```javascript
const controller = new AbortController();
const signal = controller.signal;

// Cancelar después de 5 segundos
setTimeout(() => controller.abort(), 5000);

fetch(url, { signal })
  .then(res => res.json())
  .catch(err => {
    if (err.name === 'AbortError') {
      console.log('Petición cancelada por el usuario o tiempo agotado');
    }
  });
```

---

## Consideraciones Finales

*   **Subida de archivos:** Usa un objeto `FormData` en el `body`. Fetch ajustará automáticamente el `Content-Type` correcto incluyendo el *boundary*.
*   **CORS:** Por defecto, las peticiones están sujetas a políticas de CORS. Puedes ajustar esto con la opción `mode`.
*   **Fetch vs Axios:** `fetch` es nativo y ligero, pero carece de interceptores, manejo automático de timeouts (nativo) o transformación automática de JSON que sí ofrece Axios.

---
[Volver al Índice](../js-index.md)
