
## Archivo: `04-canvas-basico.md`


El elemento <canvas> proporciona un área de dibujo de píxeles mediante scripts (API de Canvas 2D, WebGL para 3D). Aquí veremos los fundamentos del contexto 2D.
Obtener el contexto
```html
<canvas id="lienzo" width="400" height="300"></canvas>
```

```js
const canvas = document.getElementById('lienzo');
const ctx = canvas.getContext('2d');
```

### Dibujo de formas

    Rectángulos:

        fillRect(x, y, width, height): rectángulo relleno.

        strokeRect(x, y, w, h): rectángulo contorneado.

        clearRect(x, y, w, h): borra píxeles.

    Caminos (paths):
```js
    ctx.beginPath();
    ctx.moveTo(50, 50);
    ctx.lineTo(100, 100);
    ctx.lineTo(50, 100);
    ctx.closePath(); // cierra la figura
    ctx.stroke(); // dibuja la línea
    ctx.fill(); // rellena el interior
```

    Arcos/círculos:
    ctx.arc(x, y, radius, startAngle, endAngle, anticlockwise?).
    Ángulos en radianes. Ej: ctx.arc(100, 100, 50, 0, Math.PI * 2).

### Estilos de trazo y relleno

### ctx.fillStyle = 'red' | '#00FF00' | 'rgba(...)' | gradiente | patrón

    ctx.strokeStyle = ...

### ctx.lineWidth = 5

### ctx.lineCap, ctx.lineJoin

### Gradientes y patrones

    Lineal: const grad = ctx.createLinearGradient(x0,y0, x1,y1); grad.addColorStop(0, 'white'); grad.addColorStop(1, 'black');

### Radial: ctx.createRadialGradient(x0,y0,r0, x1,y1,r1)

### Patrón: ctx.createPattern(imagen, 'repeat')

### Texto

### ctx.font = '20px Arial'

### ctx.fillText('texto', x, y) (relleno)

### ctx.strokeText('texto', x, y) (contorno)

### ctx.textAlign, ctx.textBaseline

### Transformaciones

    ctx.translate(x, y): desplaza el origen.

    ctx.rotate(rad): rota el lienzo.

    ctx.scale(sx, sy): escala.

    ctx.save() y ctx.restore(): apilan y restauran el estado (transformaciones, estilos).

### Imágenes
```js
const img = new Image();
img.onload = () => ctx.drawImage(img, x, y, width?, height?);
img.src = 'ruta.png';
```

También se puede recortar con drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh).
Animaciones

Canvas no mantiene estado entre fotogramas; hay que redibujar todo en cada frame. Típico bucle:
```js
function animar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // actualizar y dibujar
  requestAnimationFrame(animar);
}
animar();
```

### Pixel manipulation

ctx.getImageData(x,y,w,h) devuelve un objeto ImageData con .data (Uint8ClampedArray en formato RGBA). Permite leer y escribir píxeles directamente. ctx.putImageData(imageData, x, y) para escribir.
Buenas prácticas

    Especificar width y height en el elemento o en js; no modificar con CSS (distorsiona).

    Limpiar el lienzo al inicio de cada frame.

    Usar requestAnimationFrame para animaciones suaves.

    Para gráficos complejos, considerar librerías como Fabric.js, PixiJS, Konva.

### 11-conceptos-avanzados
---
