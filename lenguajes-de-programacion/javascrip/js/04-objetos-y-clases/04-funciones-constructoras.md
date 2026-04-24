# Funciones Constructoras

Una función constructora es una función convencional que se invoca con el operador `new`. Su propósito principal es crear e inicializar un nuevo objeto.

## Convenciones

*   **PascalCase**: El nombre debe comenzar con mayúscula (ej. `Persona`) para distinguirla de funciones normales.
*   **Uso de `this`**: Internamente utiliza `this` para asignar propiedades al nuevo objeto.
*   **Retorno**: No debe devolver explícitamente un objeto. Si devuelve un valor primitivo, se ignora; si devuelve un objeto, ese objeto será el resultado final en lugar de la instancia creada.

## Ejemplo de Uso

```javascript
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

## ¿Qué ocurre al usar `new`?

> [!IMPORTANT]
> Cuando se ejecuta una función con el operador `new`, ocurren los siguientes pasos:
> 1. Se crea un **nuevo objeto vacío**.
> 2. El **prototipo** del nuevo objeto se enlaza a `Func.prototype`.
> 3. Dentro de la función, `this` se vincula al nuevo objeto.
> 4. Se ejecuta el cuerpo de la función (inicializando propiedades).
> 5. Si la función no retorna un objeto explícitamente, se devuelve el objeto creado automáticamente.

## Detección de llamadas con `new`

Desde ES6, podemos usar `new.target` para verificar si una función fue invocada correctamente:

*   **`new.target`**: Es una referencia a la función constructora si se llamó con `new`.
*   Si la función se llamó de forma normal, `new.target` será `undefined`.

```javascript
function Usuario() {
  if (!new.target) {
    throw new Error('Debe usar "new" para crear un usuario');
  }
}
```

## Limitaciones y Problemas

Aunque potentes, las funciones constructoras presentan algunos inconvenientes:

*   **Manejo manual de `prototype`**: Definir métodos requiere manipular el prototipo por separado, lo que puede ser confuso.
*   **Ambigüedad**: No es visualmente obvio que una función deba usarse con `new`. Si se omite, puede causar efectos colaterales inesperados en el ámbito global.
*   **Sustitución**: La sintaxis de **clases** resuelve estos problemas con un diseño más limpio y restricciones nativas.
