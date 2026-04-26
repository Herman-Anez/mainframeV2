# Clases en ES6

La sintaxis `class` introducida en ES6 proporciona una manera más clara, familiar y estructurada de crear objetos y manejar la herencia, aunque internamente sigue basándose en prototipos.

## Declaración de Clase

```javascript
class Persona {
  constructor(nombre, edad) {
    this.nombre = nombre;
    this.edad = edad;
  }

  saludar() {
    return `Hola, soy ${this.nombre}`;
  }

  static especie() {
    return 'humano';
  }
}
```

*   **`constructor`**: Método especial que se ejecuta al instanciar con `new`. Si no se define, JavaScript utiliza uno vacío por defecto.
*   **Métodos de instancia**: Se definen en el cuerpo de la clase y se añaden automáticamente al `prototype`.
*   **`static`**: Define métodos que pertenecen a la clase misma, no a las instancias.

## Herencia con `extends` y `super`

```javascript
class Estudiante extends Persona {
  constructor(nombre, edad, curso) {
    super(nombre, edad); // Debe llamarse a super antes de usar this
    this.curso = curso;
  }

  saludar() {
    return `${super.saludar()}. Estudio ${this.curso}`;
  }
}
```

*   **`extends`**: Establece la cadena de prototipos entre las clases.
*   **`super()`**: En el constructor, invoca al constructor del padre. **Es obligatorio llamarlo antes de acceder a `this`**.
*   **`super.metodo()`**: Permite acceder a métodos definidos en la clase superior.

## Miembros Privados (ES2022)

Las propiedades y métodos privados se definen prefijándolos con el símbolo `#`.

```javascript
class Cuenta {
  #saldo = 0;

  depositar(monto) {
    this.#saldo += monto;
  }

  getSaldo() {
    return this.#saldo;
  }
}
```

> [!NOTE]
> Los miembros privados no son accesibles desde fuera de la clase ni desde sus subclases, garantizando una encapsulación real.

## Campos Públicos (Class Fields)

Permiten declarar propiedades directamente en el cuerpo de la clase sin necesidad de usar `this` dentro del constructor:

```javascript
class Rectangulo {
  alto = 10;
  ancho = 5;
}
```

## Getters y Setters en Clases

Al igual que en los objetos literales, las clases permiten el uso de `get` y `set` para interceptar el acceso a propiedades.

## Diferencias con Funciones Constructoras

> [!IMPORTANT]
> Aunque parezcan similares, las clases tienen reglas más estrictas:
> 1. **Modo Estricto**: Todo el código dentro de una clase se ejecuta automáticamente en `strict mode`.
> 2. **Llamada Obligatoria con `new`**: No se pueden invocar como funciones normales; lanzarán un `TypeError`.
> 3. **Hoisting**: Las clases no tienen *hoisting* (elevación) total; se encuentran en la Zona Muerta Temporal (TDZ) hasta su declaración.

## Resumen

Las clases no reemplazan el modelo de prototipos; son una capa de "azúcar sintáctico" que facilita la programación orientada a objetos (POO) en JavaScript, haciendo el código más legible y mantenible.
---
[back](../index)
