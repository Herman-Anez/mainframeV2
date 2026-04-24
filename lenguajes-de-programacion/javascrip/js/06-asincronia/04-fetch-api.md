## Archivo: `04-fetch-api.md`


fetch es la API moderna para realizar peticiones HTTP en el navegador (y disponible globalmente en Node 18+). Retorna una Promesa que resuelve un objeto Response.
Sintaxis básica
```js
fetch(url, options)
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('Error de red o parseo', error));

```
    url: string o URL.

    options: objeto de configuración opcional (method, headers, body, mode, etc.).

    Por defecto realiza GET.

### El objeto Response

Propiedades principales:

    response.ok: booleano, true si status entre 200-299.

    response.status: código HTTP (200, 404...).

    response.headers: objeto Headers.

    response.url: URL final después de redirecciones.
    Métodos para leer el cuerpo (solo uno puede ser llamado, el cuerpo se consume):

    response.json(): parsea JSON.

    response.text(): texto plano.

    response.blob(): datos binarios (imágenes, archivos).

    response.arrayBuffer(): buffer de bytes.

    response.formData(): para datos de formulario.

### Configuración de peticiones
```js
fetch('/api/item', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
  },
  body: JSON.stringify({ nombre: 'Producto' })
})
```

Otras opciones: mode ('cors', 'no-cors', 'same-origin'), credentials ('include', 'same-origin', 'omit'), cache, redirect.
Manejo de errores

fetch solo rechaza la promesa por errores de red (no se pudo conectar). Un status HTTP 404 o 500 NO es un error de red, la promesa se resuelve normalmente. Por eso es necesario verificar response.ok.
Cancelación con AbortController

Se puede cancelar una petición fetch usando AbortController.
```js
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
fetch(url, { signal: controller.signal })
  .then(...)
  .catch(err => {
    if (err.name === 'AbortError') console.log('Cancelada');
  });
```

### Subida de archivos

body puede ser un FormData para subir archivos:
```js
const formData = new FormData();
formData.append('archivo', fileInput.files[0]);
fetch('/upload', { method: 'POST', body: formData });
```

### Streaming

El cuerpo de la respuesta puede ser leído como stream usando response.body.getReader(), útil para grandes descargas.
Fetch vs Axios

Fetch es nativo, no necesita dependencias, pero carece de algunas comodidades como interceptores, timeout nativo (se puede con AbortController) o manejo automático de JSON. Axios sigue siendo popular en proyectos grandes.
---
