# Canvas API (Fundamentos 2D)

El elemento `<canvas>` proporciona un área de dibujo basada en píxeles que se manipula mediante scripts. Es ideal para gráficos dinámicos, juegos y visualización de datos.

---

## Obtener el contexto

Para dibujar, primero definimos el elemento en HTML y luego obtenemos su contexto de dibujo en JavaScript.

```html
<canvas id="lienzo" width="400" height="300"></canvas>
```

```js
const canvas = document.getElementById('lienzo');
const ctx = canvas.getContext('2d');
```

---

## Dibujo de formas básicas

### Rectángulos
- **`fillRect(x, y, w, h)`**: Dibuja un rectángulo relleno.
- **`strokeRect(x, y, w, h)`**: Dibuja el contorno de un rectángulo.
- **`clearRect(x, y, w, h)`**: Borra los píxeles en el área especificada (los hace transparentes).

### Caminos (*Paths*)
Para crear formas complejas, se definen rutas de puntos:

```js
ctx.beginPath();       // Inicia un nuevo camino
ctx.moveTo(50, 50);    // Mueve el "lápiz" a una posición
ctx.lineTo(100, 100);  // Dibuja una línea hasta otra posición
ctx.lineTo(50, 100);
ctx.closePath();       // Cierra la figura volviendo al inicio
ctx.stroke();          // Dibuja el contorno
ctx.fill();            // Rellena el interior
```

### Arcos y Círculos
`ctx.arc(x, y, radio, anguloInicio, anguloFin, sentidoAntihorario?)`
*Nota: Los ángulos se miden en **radianes**.*

---

## Estilos y Colores

- **`ctx.fillStyle`**: Color de relleno (nombres, hex, RGB, gradientes).
- **`ctx.strokeStyle`**: Color del contorno.
- **`ctx.lineWidth`**: Grosor de la línea.
- **`ctx.lineCap`**: Estilo de los extremos de la línea (`butt`, `round`, `square`).

### Gradientes y Patrones
- **Lineal:** `const grad = ctx.createLinearGradient(x0, y0, x1, y1);`
- **Radial:** `ctx.createRadialGradient(x0, y0, r0, x1, y1, r1);`
- **Patrón:** `ctx.createPattern(imagen, 'repeat');`

---

## Texto

```js
ctx.font = '20px Arial';
ctx.fillText('Hola Canvas', x, y);   // Texto relleno
ctx.strokeText('Hola Canvas', x, y); // Contorno de texto
```

---

## Transformaciones

Permiten modificar cómo se dibuja en el lienzo de forma global:
- **`translate(x, y)`**: Desplaza el punto de origen (0,0).
- **`rotate(radianes)`**: Rota el lienzo alrededor del origen.
- **`scale(x, y)`**: Escala los dibujos.

> [!TIP]
> Usa **`ctx.save()`** antes de aplicar transformaciones y **`ctx.restore()`** al terminar. Esto permite guardar y recuperar el estado original (estilos, posición, etc.) del contexto.

---

## Imágenes

```js
const img = new Image();
img.src = 'ruta.png';
img.onload = () => {
  ctx.drawImage(img, x, y, width, height);
};
```
*También es posible recortar imágenes usando los 9 parámetros de `drawImage`.*

---

## Animaciones

El lienzo es un mapa de bits estático; para animar, debemos borrar y redibujar todo el contenido en cada fotograma.

```js
function animar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // 1. Actualizar posiciones
  // 2. Dibujar elementos
  requestAnimationFrame(animar); // Sincroniza con el refresco de pantalla
}
animar();
```

---

## Manipulación de Píxeles

`ctx.getImageData(x, y, w, h)` devuelve un objeto `ImageData` con una propiedad `.data` (un `Uint8ClampedArray` en formato **RGBA**). Esto permite procesar imágenes píxel a píxel a nivel de bajo nivel.

---

## Buenas prácticas

- **Dimensiones:** Define siempre el `width` y `height` directamente en el atributo del elemento o mediante JS. Evita usar CSS para cambiar el tamaño, ya que esto escala la imagen y causa distorsión.
- **Optimización:** Limpia el lienzo al inicio de cada frame de animación para evitar rastros.
- **Librerías:** Para proyectos complejos de juegos o escenas interactivas, considera usar librerías como **Fabric.js**, **PixiJS** o **Konva**.
### 11-conceptos-avanzados
---

---
[back](../index)
