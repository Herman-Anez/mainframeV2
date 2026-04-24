


## Archivo: `06-web-workers.md`


Los Web Workers permiten ejecutar código js en un hilo separado del hilo principal (UI), evitando bloqueos. Se comunican con el hilo principal mediante mensajes.
Tipos de workers

    Dedicated Worker: dedicado al script que lo crea. La comunicación es 1:1.

    Shared Worker: puede ser compartido por varias pestañas/orígenes del mismo origen. Comunicación a través de puertos.

    Service Worker: funciona como proxy de red, permite offline, notificaciones push. Sigue un ciclo de vida especial y actúa a nivel de dominio.

Aquí nos centramos en el Dedicated Worker.
Crear un worker
```js
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ type: 'start', data: [1,2,3] });
```

### worker.onmessage = (e) => {
  console.log('Resultado:', e.data);
};

### worker.onerror = (e) => {
  console.error('Error en worker:', e.message);
};

### // worker.js
self.onmessage = (e) => {
  const result = e.data.data.reduce((a,b) => a+b, 0);
  self.postMessage(result);
};

### Intercambio de mensajes

    postMessage permite pasar datos que son copiados (structured clone algorithm).

    Se pueden transferir ciertos objetos (ArrayBuffer, MessagePort, ImageBitmap) mediante transferencia de propiedad (movimiento, no copia), liberando el original en el emisor. Esto se logra pasando un segundo argumento: worker.postMessage(buffer, [buffer]).

### APIs disponibles en Workers

Los workers tienen acceso limitado:

    No pueden manipular el DOM, ni acceder a window, document, parent.

    Disponen de self, importScripts() (para cargar otros scripts), fetch, XMLHttpRequest, WebSocket, IndexedDB.

    Pueden usar navigator, location (solo lectura), setTimeout/setInterval.

    Pueden crear otros workers (subworkers).

### Terminación

    worker.terminate() desde el hilo principal finaliza el worker inmediatamente.

    self.close() desde dentro del worker lo cierra.

### Casos de uso

    Operaciones de CPU intensiva: procesamiento de imágenes, cálculos matemáticos, criptografía.

    Parseo y manipulación de grandes datos (CSV, JSON).

    Simulaciones y motores de juego.

    Prefetching y procesamiento de datos en segundo plano.

### Errores y depuración

    Los errores no capturados en el worker no afectan al hilo principal; se reportan mediante onerror.

    Las herramientas de desarrollo del navegador pueden inspeccionar workers y ver sus consolas.

### Consideraciones

    La creación de muchos workers puede consumir mucha memoria; cada worker tiene su propio heap.

    La comunicación mediante serialización puede ser costosa para grandes volúmenes; usar transferencia de buffers para datos binarios.

    Para tareas pequeñas, el coste de crear un worker puede superar el beneficio; evaluar con medidas de rendimiento.

### Shared Workers y Service Workers

    Shared Workers: mismo script accedido por múltiples conexiones (pestañas). Cada conexión usa un MessagePort.

    Service Workers: actúan como proxy de red, interceptan peticiones fetch, manejan caché, notificaciones push y sincronización en fondo. Tienen ciclo de vida (instalación, activación) y requieren HTTPS.
