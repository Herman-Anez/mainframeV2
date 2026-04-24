
## Archivo: `05-clases-es6.md`


La sintaxis class introduce una manera más clara y familiar de crear objetos y manejar la herencia, basada internamente en prototipos.
Declaración de clase
```js
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

    El método constructor se ejecuta al hacer new Persona(...). Si no se define, se usa uno vacío por defecto.

    Los métodos definidos en el cuerpo de la clase van al prototype (no son propios de cada instancia).

    static define un método en la propia clase (no en las instancias).
```

### Herencia con extends y super
```js
class Estudiante extends Persona {
  constructor(nombre, edad, curso) {
    super(nombre, edad); // debe llamarse a super antes de usar this
    this.curso = curso;
  }
  saludar() {
    return `${super.saludar()}. Estudio ${this.curso}`;
  }
}

    extends establece la cadena de prototipos (tanto Estudiante.prototype como Estudiante.__proto__).

    super dentro del constructor invoca al constructor padre.

    super.metodo() llama a la versión del padre de un método.
```

### Miembros privados (ES2022)

Se prefijan con #. No son accesibles fuera de la clase.
```js
class Cuenta {
  #saldo = 0;
  depositar(monto) {
    this.#saldo += monto;
  }
  getSaldo() {
    return this.#saldo;
  }
}

    No pueden ser accedidos ni desde subclases (a menos que se expongan mediante métodos protegidos, no nativos).
```

### Campos públicos (class fields)

Las propiedades pueden declararse directamente en el cuerpo de la clase (sin this en el constructor) y se inicializan antes del constructor:
```js
class Rectangulo {
  alto = 10;
  ancho = 5;
  area = this.alto * this.ancho; // cuidado: se evalúa cuando se crea la instancia
}
```

Estos campos son propios de la instancia.
Getters y setters en clases

Igual que en objetos literales, con get y set.
Diferencias con funciones constructoras

    El código de una clase siempre se ejecuta en modo estricto.

    Las clases no se pueden llamar sin new (error TypeError).

    Las declaraciones de clase no son izadas (hoisting temporal pero con TDZ, a diferencia de las funciones que si se elevan).

### Resumen

Las clases no reemplazan los prototipos; son un envoltorio sintáctico que facilita la programación orientada a objetos en js, especialmente para desarrolladores que vienen de lenguajes basados en clases.