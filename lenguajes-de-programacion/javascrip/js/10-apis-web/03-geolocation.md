## Archivo: `03-geolocation.md`


La Geolocation API permite obtener la ubicación del dispositivo con el consentimiento del usuario.
Objeto navigator.geolocation

Disponible solo en contextos seguros (HTTPS). Métodos principales:
getCurrentPosition(success, error?, options?)

Obtiene la posición una sola vez.
```js
navigator.geolocation.getCurrentPosition(
  (position) => {
    console.log(position.coords.latitude, position.coords.longitude);
  },
  (error) => {
    console.error('Error:', error.message);
  },
  { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
);
```

Propiedades del objeto position.coords:

### latitude, longitude (grados decimales)

### accuracy (metros), altitude, altitudeAccuracy, heading, speed

### watchPosition(success, error?, options?)

Registra un vigilante que llama al callback cada vez que la posición cambia. Devuelve un watchId.
clearWatch(watchId)

Detiene el seguimiento iniciado con watchPosition.
Opciones

    enableHighAccuracy: booleano, solicita GPS más preciso (puede consumir más batería).

    timeout: ms máximos para obtener posición.

    maximumAge: tiempo máximo en ms de una caché permitida (0 = siempre nueva).

### Errores

El callback de error recibe un objeto GeolocationPositionError con:

    code: 1 (PERMISSION_DENIED), 2 (POSITION_UNAVAILABLE), 3 (TIMEOUT).

    message: texto descriptivo.

### Permisos

El navegador pide permiso explícito al usuario. Con la API Permissions se puede consultar el estado (pero no se puede solicitar programáticamente sin un gesto del usuario previo).
Limitaciones

    Solo funciona en HTTPS.

    La precisión varía (GPS en exteriores, WiFi/móvil en interiores).

    No disponible en todos los dispositivos (siempre verificar if ('geolocation' in navigator)).

### Casos de uso

    Mapas y servicios basados en localización.

    Búsqueda de lugares cercanos.

    Registro de rutas.

---
