## Archivo: `02-clipboard.md`


La Clipboard API permite leer y escribir en el portapapeles del sistema de forma asíncrona y segura, reemplazando al antiguo document.execCommand('copy').
Escritura en portapapeles
```js
await navigator.clipboard.writeText('Texto a copiar');
```

O para datos binarios:
```js
const blob = new Blob(['<h1>HTML</h1>'], { type: 'text/html' });
const item = new ClipboardItem({ 'text/html': blob });
await navigator.clipboard.write([item]);
```

ClipboardItem permite múltiples representaciones (texto plano + HTML, por ejemplo) para que el destino pegue la que prefiera.
Lectura del portapapeles
```js
const texto = await navigator.clipboard.readText();
```

Para leer otros formatos:
```js
const items = await navigator.clipboard.read();
for (const item of items) {
  for (const type of item.types) {
    const blob = await item.getType(type);
    // procesar blob (texto, imagen, etc.)
  }
}
```

### Permisos y seguridad

    La escritura requiere interacción del usuario (clic, tecla) o permiso clipboard-write. En páginas seguras (HTTPS) normalmente se concede implícitamente en respuesta a un gesto del usuario.

    La lectura requiere el permiso clipboard-read, solicitado con la API Permissions:

```js
const permiso = await navigator.permissions.query({ name: 'clipboard-read' });
if (permiso.state === 'granted' || permiso.state === 'prompt') {
  const texto = await navigator.clipboard.readText();
}

    Ambas requieren contexto seguro (HTTPS o localhost).
```

### Eventos copy, cut, paste

Se pueden interceptar en el documento para modificar los datos que se copian o pegan. Ejemplo para añadir información extra al copiar:
```js
document.addEventListener('copy', (e) => {
  e.preventDefault();
  const seleccion = document.getSelection().toString();
  e.clipboardData.setData('text/plain', seleccion + '\n\nFuente: mi web');
});
```

### Consideraciones

    La API asíncrona no está disponible en todos los navegadores antiguos.

    Siempre manejar excepciones: el acceso puede ser denegado.

    No dependas de que el portapapeles esté accesible; ofrece alternativas.

---
