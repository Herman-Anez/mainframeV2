## Archivo: `04-web-storage.md`


El almacenamiento web permite guardar datos en el navegador de forma sencilla, sin cookies y con mayor capacidad.
localStorage

    Almacenamiento persistente: los datos sobreviven cierres del navegador y reinicios.

    Espacio típico: ~5-10 MB por origen.

    API síncrona y sencilla.

```js
// Guardar
localStorage.setItem('usuario', JSON.stringify({ nombre: 'Ana' }));
// Leer
const usuario = JSON.parse(localStorage.getItem('usuario'));
// Eliminar uno
localStorage.removeItem('usuario');
// Limpiar todo
localStorage.clear();
// Iterar
for (let i = 0; i < localStorage.length; i++) {
  const clave = localStorage.key(i);
  const valor = localStorage.getItem(clave);
}
```

    Solo almacena strings. Para objetos usa JSON.stringify/parse.

    Acceso por origen (protocolo + dominio + puerto).

    Las operaciones son síncronas, no bloquean significativamente porque leen/escriben en disco rápido. Para grandes cantidades puede bloquear, mejor usar IndexedDB.

### sessionStorage

Idéntico a localStorage en API, pero los datos se eliminan al cerrar la pestaña o ventana. Cada pestaña tiene su propio almacenamiento aislado (incluso si comparten origen).

Útil para datos de sesión, como formularios temporales, pasos de wizard, etc.
Evento storage

Se dispara en todas las demás pestañas/orígenes (no en la que realizó el cambio) cuando localStorage o sessionStorage es modificado. Permite sincronizar estado entre pestañas.
```js
window.addEventListener('storage', (e) => {
  console.log(`Clave ${e.key} cambió de ${e.oldValue} a ${e.newValue}`);
  console.log('Origen:', e.url);
});
```

sstorageArea distingue si el cambio fue en localStorage o sessionStorage.
Capacidades y límites

    Almacenamiento por origen (~5-10MB, variable).

    Exceder el límite lanza QuotaExceededError.

    No apto para datos sensibles (no está cifrado, XSS puede acceder).

    No es un sustituto de bases de datos, para datos estructurados complejos usar IndexedDB.

    No bloquea el hilo en exceso pero puede ralentizar si se abusa.

### Buenas prácticas

    Siempre usar JSON.stringify y JSON.parse.

    Capturar excepciones de cuota (try/catch).

    Prefijar las claves para evitar colisiones.

    No almacenar tokens de sesión o información sensible; preferir cookies HttpOnly y Secure.

    Para datos que cambian muy frecuentemente, considerar usar en memoria y persistir solo ocasionalmente.

### Cookies vs Web Storage
Característica	Cookies	Web Storage
Capacidad	~4KB	~5-10MB
Envío al servidor	Sí (automático en cada petición)	No (solo accesible por JS)
Persistencia	Configurable (expira)	localStorage persiste, sessionStorage no
Accesibilidad	document.cookie	API sencilla

Para estado de interfaz y datos no críticos, web storage es ideal.

### 09-módulos
---
