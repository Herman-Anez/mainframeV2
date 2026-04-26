# Geolocation API

La **Geolocation API** permite a las aplicaciones web obtener la ubicación geográfica del dispositivo del usuario, siempre que este otorgue su consentimiento explícito.

---

## El objeto `navigator.geolocation`

Esta API solo está disponible en contextos seguros (**HTTPS**). Proporciona tres métodos principales para gestionar la ubicación:

### 1. `getCurrentPosition(success, error, options)`

Obtiene la ubicación actual del dispositivo una sola vez.

```js
const options = {
  enableHighAccuracy: true,
  timeout: 10000,
  maximumAge: 60000
};

navigator.geolocation.getCurrentPosition(
  (position) => {
    const { latitude, longitude, accuracy } = position.coords;
    console.log(`Latitud: ${latitude}, Longitud: ${longitude}`);
    console.log(`Precisión: ${accuracy} metros`);
  },
  (error) => {
    console.error(`Error (${error.code}): ${error.message}`);
  },
  options
);
```

### 2. `watchPosition(success, error, options)`

Registra un "vigilante" que ejecuta el callback de éxito cada vez que la posición del dispositivo cambia. Devuelve un identificador (`watchId`).

### 3. `clearWatch(watchId)`

Detiene el seguimiento de la ubicación iniciado previamente con `watchPosition`.

---

## Propiedades de `coords`

El objeto `position.coords` devuelto contiene información detallada:

- **`latitude` / `longitude`**: Coordenadas en grados decimales.
- **`accuracy`**: Nivel de precisión de la latitud y longitud en metros.
- **`altitude`**: Altitud sobre el nivel del mar (puede ser `null`).
- **`speed`**: Velocidad actual en metros por segundo (puede ser `null`).
- **`heading`**: Dirección del movimiento en grados (0-360).

---

## Opciones de configuración

- **`enableHighAccuracy`**: Booleano. Si es `true`, solicita la mejor precisión posible (usualmente activando el GPS), lo que puede aumentar el consumo de batería y el tiempo de respuesta.
- **`timeout`**: Tiempo máximo (en ms) permitido para intentar obtener la posición.
- **`maximumAge`**: Tiempo máximo (en ms) que el navegador puede usar una posición almacenada en caché.

---

## Gestión de Errores

El callback de error recibe un objeto `GeolocationPositionError` con los siguientes códigos:

- `1` (**PERMISSION_DENIED**): El usuario rechazó la solicitud de ubicación.
- `2` (**POSITION_UNAVAILABLE**): El dispositivo no pudo determinar la ubicación (ej: falta de señal).
- `3` (**TIMEOUT**): Se alcanzó el tiempo límite establecido en las opciones.

---

## Consideraciones y Limitaciones

> [!IMPORTANT]
> **Privacidad:** El navegador siempre mostrará un aviso al usuario solicitando permiso. No es posible forzar la obtención de la ubicación sin la aprobación manual del usuario.

- **Seguridad:** Requisito obligatorio de **HTTPS**.
- **Disponibilidad:** Siempre verifica si la API existe en el navegador antes de usarla: `if ('geolocation' in navigator)`.
- **Variabilidad:** La precisión depende del hardware (GPS, WiFi, antenas de telefonía) y del entorno (interiores vs. exteriores).

---

## Casos de uso comunes

1. Visualización de mapas y navegación en tiempo real.
2. Localización de tiendas o servicios cercanos (*POIs*).
3. Etiquetado geográfico de contenido o registros de actividad física.

---
[back](../index)
