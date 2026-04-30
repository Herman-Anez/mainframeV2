# Web Storage API

La API de **Web Storage** proporciona mecanismos para que los navegadores almacenen pares clave-valor de una forma mucho más intuitiva y con mayor capacidad que las tradicionales cookies.

---

## localStorage

`localStorage` permite almacenar datos de forma persistente en el navegador del usuario. Los datos no tienen fecha de expiración y permanecen allí incluso después de cerrar la pestaña o reiniciar el ordenador.

```javascript
// Guardar un objeto (debe convertirse a string)
const usuario = { id: 1, nombre: 'Ana' };
localStorage.setItem('usuario_activo', JSON.stringify(usuario));

// Recuperar y parsear el objeto
const datosGuardados = localStorage.getItem('usuario_activo');
if (datosGuardados) {
  const usuarioCargado = JSON.parse(datosGuardados);
  console.log(usuarioCargado.nombre); // "Ana"
}

// Eliminar un elemento o limpiar todo
localStorage.removeItem('usuario_activo');
localStorage.clear();
```

> [!IMPORTANT]
> Web Storage solo almacena **cadenas de texto (strings)**. Es imprescindible usar `JSON.stringify()` al guardar y `JSON.parse()` al recuperar para manejar objetos y arrays.

---

## sessionStorage

Funciona exactamente igual que `localStorage` en cuanto a su API y métodos, pero con una diferencia clave en su persistencia: **los datos se eliminan cuando finaliza la sesión de la página**.

*   La sesión dura mientras la pestaña o ventana esté abierta.
*   Abrir la misma página en una pestaña nueva crea una sesión nueva (aislada).
*   **Uso ideal:** Datos temporales como el estado de un formulario de varios pasos o filtros de búsqueda.

---

## El Evento `storage`

Este evento es fundamental para la sincronización entre pestañas. Se dispara en todas las ventanas o pestañas del **mismo origen** cuando se modifica el almacenamiento (excepto en la pestaña que realizó el cambio).

```javascript
window.addEventListener('storage', (event) => {
  console.log(`Clave modificada: ${event.key}`);
  console.log(`Valor anterior: ${event.oldValue}`);
  console.log(`Valor nuevo: ${event.newValue}`);
  console.log(`Origen del cambio: ${event.url}`);
});
```

---

## Capacidades y Seguridad

### Límites de Almacenamiento
Típicamente, el navegador permite entre **5MB y 10MB** por origen. Si se excede este límite, el navegador lanzará un error de tipo `QuotaExceededError`.

### Seguridad (XSS)
> [!CAUTION]
> **No guardes información sensible** (como contraseñas o tokens de sesión críticos) en Web Storage. Cualquier script ejecutado en tu página tiene acceso total a estos datos, lo que los hace vulnerables a ataques de Cross-Site Scripting (XSS).

---

## Comparativa: Cookies vs Web Storage

| Característica | Cookies | Web Storage |
| :--- | :--- | :--- |
| **Capacidad** | ~4 KB | ~5-10 MB |
| **Persistencia** | Configurable (Expira) | `localStorage` (Indefinido) |
| **Tráfico HTTP** | Se envían en cada petición | Solo residen en el cliente |
| **API** | Compleja (`document.cookie`) | Sencilla (`setItem`, `getItem`) |

---

## Buenas Prácticas

1.  **Manejo de Errores:** Envuelve las llamadas a `.setItem()` en un bloque `try...catch` para gestionar casos donde el almacenamiento esté lleno.
2.  **Prefijos de Claves:** Usa prefijos (ej. `app_config_`) para evitar colisiones con otros scripts o librerías de terceros.
3.  **No sobrecargar:** No uses Web Storage como una base de datos de alto rendimiento. Para datos masivos o complejos, considera usar **IndexedDB**.
4.  **Limpieza:** Elimina los datos que ya no sean necesarios para no ocupar espacio innecesario en el dispositivo del usuario.

---
[Volver al Índice](../js-index.md)
