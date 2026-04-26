# Web Storage API

El almacenamiento web permite guardar datos en el navegador de forma sencilla, con mayor capacidad que las cookies y sin necesidad de enviarlos en cada petición HTTP.

---

## `localStorage`

- **Persistencia:** Los datos sobreviven al cierre del navegador y reinicios del sistema.
- **Capacidad:** Típicamente entre 5-10 MB por origen.
- **API:** Síncrona y basada en pares clave-valor.

```js
// Guardar datos
localStorage.setItem('usuario', JSON.stringify({ nombre: 'Ana' }));

// Leer datos
const usuario = JSON.parse(localStorage.getItem('usuario'));

// Eliminar un elemento específico
localStorage.removeItem('usuario');

// Limpiar todo el almacenamiento del origen
localStorage.clear();

// Iterar sobre las claves
for (let i = 0; i < localStorage.length; i++) {
  const clave = localStorage.key(i);
  const valor = localStorage.getItem(clave);
  console.log(clave, valor);
}
```

> [!NOTE]
> Solo almacena **strings**. Para guardar objetos o arrays, es imprescindible usar `JSON.stringify()` al guardar y `JSON.parse()` al recuperar. El acceso está restringido por **Same-Origin Policy** (protocolo + dominio + puerto).

---

## `sessionStorage`

Es idéntico a `localStorage` en cuanto a su API y métodos, pero con una diferencia fundamental en su ciclo de vida: **los datos se eliminan al cerrar la pestaña o ventana**.

- Cada pestaña abierta tiene su propio `sessionStorage` aislado, incluso si cargan la misma URL.
- **Uso ideal:** Datos temporales de la sesión, estados de formularios en varios pasos (*wizards*) o filtros de búsqueda efímeros.

---

## El evento `storage`

Se dispara en todas las **otras** pestañas del mismo origen cuando ocurre un cambio en `localStorage` o `sessionStorage`. Es fundamental para sincronizar el estado de la aplicación en tiempo real.

```js
window.addEventListener('storage', (e) => {
  console.log(`La clave "${e.key}" cambió de "${e.oldValue}" a "${e.newValue}"`);
  console.log('URL del cambio:', e.url);
});
```

---

## Capacidades y límites

- **Límites de cuota:** Exceder el espacio asignado por el navegador lanzará un `QuotaExceededError`.
- **Seguridad:** No es apto para datos sensibles (tokens de sesión críticos, PII) ya que cualquier script en la página (incluyendo posibles ataques XSS) puede acceder a ellos.
- **Alternativas:** Para datos estructurados complejos o grandes volúmenes, se recomienda usar **IndexedDB**.

---

## Buenas prácticas

- **Serialización:** Usa siempre `JSON.stringify` y `JSON.parse`.
- **Gestión de errores:** Envuelve las escrituras en bloques `try/catch` para capturar errores de cuota.
- **Nombres de clave:** Prefija tus claves (ej: `myapp_user`) para evitar colisiones con otros scripts.
- **Seguridad:** No almacenes información sensible. Para tokens de autenticación, prefiere **cookies** con las banderas `HttpOnly` y `Secure`.

---

## Cookies vs Web Storage

| Característica | Cookies | Web Storage |
| :--- | :--- | :--- |
| **Capacidad** | ~4 KB | ~5-10 MB |
| **Envío al servidor** | Automático en cada petición | No (solo accesible vía JS) |
| **Persistencia** | Configurable (fecha expiración) | `localStorage` es permanente |
| **Accesibilidad** | `document.cookie` (complejo) | API sencilla y directa |

---

> [!TIP]
> Web Storage es ideal para mantener el estado de la interfaz y datos no críticos que mejoran la experiencia del usuario sin sobrecargar el tráfico de red.

---
[back](../index)
