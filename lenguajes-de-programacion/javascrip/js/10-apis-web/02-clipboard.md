# Clipboard API

La **Clipboard API** permite leer y escribir en el portapapeles del sistema operativo de forma asíncrona y segura. Esta API moderna reemplaza al antiguo y limitado método `document.execCommand('copy')`.

---

## Escritura en el portapapeles

### Copiar texto simple
```js
await navigator.clipboard.writeText('Texto a copiar');
```

### Copiar datos binarios o enriquecidos
Para copiar otros formatos (como HTML o imágenes), se utiliza la clase `ClipboardItem`.

```js
const blob = new Blob(['<h1>Contenido HTML</h1>'], { type: 'text/html' });
const item = new ClipboardItem({ 'text/html': blob });

await navigator.clipboard.write([item]);
```

> [!NOTE]
> `ClipboardItem` permite incluir múltiples representaciones del mismo dato (por ejemplo, texto plano y HTML simultáneamente) para que la aplicación donde se pegue el contenido elija el formato que prefiera.

---

## Lectura del portapapeles

### Leer texto simple
```js
const texto = await navigator.clipboard.readText();
```

### Leer formatos complejos
```js
const items = await navigator.clipboard.read();

for (const item of items) {
  for (const type of item.types) {
    const blob = await item.getType(type);
    // Procesar el blob según su tipo (text/plain, image/png, etc.)
  }
}
```

---

## Permisos y Seguridad

El acceso al portapapeles es una operación sensible que requiere condiciones estrictas:

- **Contexto Seguro:** Solo funciona en sitios servidos bajo **HTTPS** (o `localhost`).
- **Interacción del Usuario:** La escritura normalmente requiere un gesto del usuario (como un clic en un botón).
- **API de Permisos:** La lectura requiere que el usuario conceda explícitamente el permiso `clipboard-read`.

```js
const permiso = await navigator.permissions.query({ name: 'clipboard-read' });

if (permiso.state === 'granted' || permiso.state === 'prompt') {
  const texto = await navigator.clipboard.readText();
}
```

---

## Eventos `copy`, `cut` y `paste`

Es posible interceptar estos eventos en el documento para modificar los datos que se transfieren.

```js
document.addEventListener('copy', (e) => {
  e.preventDefault(); // Evita la copia automática
  const seleccion = document.getSelection().toString();
  
  // Añadimos metadatos o modificamos el contenido
  e.clipboardData.setData('text/plain', seleccion + '\n\nFuente: Mi Sitio Web');
});
```

---

## Consideraciones importantes

> [!WARNING]
> La API asíncrona no está disponible en navegadores muy antiguos. Siempre verifica la compatibilidad mediante `if (navigator.clipboard)`.

- **Manejo de Errores:** Utiliza bloques `try/catch` ya que el acceso puede ser denegado por el usuario o bloqueado por el navegador.
- **Alternativas:** No asumas que el portapapeles siempre estará disponible; ofrece mecanismos alternativos de visualización de datos si el acceso falla.

---
[back](../index)
