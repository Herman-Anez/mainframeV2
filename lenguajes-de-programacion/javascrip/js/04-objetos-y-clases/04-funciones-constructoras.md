## Archivo: `04-funciones-constructoras.md`


Una función constructora es una función normal que se invoca con el operador new. Su propósito es crear e inicializar un objeto.
Convención

    Nombre en PascalCase (primera letra mayúscula) para distinguirla de funciones normales.

    Internamente usa this para asignar propiedades al nuevo objeto.

    No debe devolver explícitamente un objeto (si devuelve un valor primitivo, se ignora; si devuelve un objeto, ese objeto será el resultado en lugar de la instancia).

```js
function Coche(marca, modelo) {
  this.marca = marca;
  this.modelo = modelo;
}
Coche.prototype.arrancar = function() {
  return `${this.marca} ${this.modelo} arrancado`;
};

const coche1 = new Coche('Toyota', 'Yaris');
console.log(coche1.arrancar()); // Toyota Yaris arrancado
```

### Qué ocurre al usar new

    Se crea un nuevo objeto vacío.

    El prototipo del nuevo objeto se enlaza a Func.prototype.

    Dentro de la función, this apunta al nuevo objeto.

    Se ejecuta el cuerpo de la función (normalmente para añadir propiedades).

    Si la función no retorna un objeto, se devuelve el nuevo objeto creado.

### Cómo detectar si una función fue llamada con new

    new.target: dentro de la función, si fue llamada con new es una referencia a la función constructora; si no, es undefined.

    Con eso se puede lanzar un error si se omite new.

### Problemas

    Requiere manejar el prototype para métodos, lo que puede ser confuso.

    No es obvio que deba usarse new; se puede invocar sin new, causando efectos laterales en el ámbito global.

    La sintaxis de clases resuelve estos problemas con un diseño más claro.

---
