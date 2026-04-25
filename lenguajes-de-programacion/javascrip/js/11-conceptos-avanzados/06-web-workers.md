

# Web Workers

Los **Web Workers** permiten ejecutar código JavaScript en un hilo separado del hilo principal (UI Thread). Esto es fundamental para realizar tareas pesadas sin congelar la interfaz de usuario.

---

## Tipos de Workers

- **Dedicated Workers:** Instanciados por un script principal y dedicados exclusivamente a él. La comunicación es 1:1.
- **Shared Workers:** Pueden ser accedidos por múltiples scripts (pestañas, iframes) del mismo origen.
- **Service Workers:** Actúan como proxies de red entre el navegador y el servidor. Permiten funcionalidades offline, notificaciones push y almacenamiento en caché.

---

## Implementación de un Dedicated Worker

### 1. Hilo Principal (`main.js`)
```js
const worker = new Worker('worker.js');

// Enviar datos al worker
worker.postMessage({ type: 'CALCULAR', data: [10, 20, 30] });

// Escuchar respuesta del worker
worker.onmessage = (event) => {
  console.log('Resultado recibido:', event.data);
};

// Manejo de errores
worker.onerror = (error) => {
  console.error('Error en el Worker:', error.message);
};
```

### 2. El Worker (`worker.js`)
```js
// El contexto global es 'self', no 'window'
self.onmessage = (event) => {
  const { type, data } = event.data;

  if (type === 'CALCULAR') {
    const resultado = data.reduce((acc, val) => acc + val, 0);
    // Enviar de vuelta al hilo principal
    self.postMessage(resultado);
  }
};
```

---

## Comunicación y Transferencia de Datos

Por defecto, los datos enviados mediante `postMessage` se copian usando el algoritmo de **Structured Clone**.

> [!TIP]
> Para datos muy grandes (como imágenes o grandes arrays binarios), puedes usar **Transferable Objects** (ej: `ArrayBuffer`). Esto transfiere la propiedad de la memoria al worker en lugar de copiarla, lo que es instantáneo y ahorra recursos.
> `worker.postMessage(buffer, [buffer]);`

---

## Limitaciones y Entorno del Worker

Los Web Workers se ejecutan en un entorno aislado.

### ❌ No tienen acceso a:
- El DOM (no puedes manipular elementos directamente).
- El objeto `window` o `document`.
- La mayoría de las APIs visuales.

### ✅ Sí tienen acceso a:
- `self` (su propio contexto global).
- `navigator` y `location` (solo lectura).
- `fetch` y `XMLHttpRequest`.
- `setTimeout` / `setInterval`.
- **IndexedDB**.
- Cargar otros scripts mediante `importScripts()`.

---

## Ciclo de Vida y Terminación

- **Desde el hilo principal:** `worker.terminate()` finaliza el worker inmediatamente.
- **Desde el worker:** `self.close()` permite que el worker se cierre a sí mismo una vez terminada su tarea.

---

## Casos de Uso Comunes

> [!IMPORTANT]
> No uses Web Workers para tareas pequeñas, ya que la sobrecarga de crear el hilo y serializar los mensajes puede ser mayor que el ahorro de tiempo.

1. **Procesamiento de imágenes/video:** Aplicar filtros o compresión.
2. **Criptografía:** Generación de claves o hashing pesado.
3. **Grandes cálculos:** Análisis de Big Data o simulaciones físicas.
4. **Parsing de datos:** Procesar archivos CSV o JSON de gran tamaño en segundo plano.
