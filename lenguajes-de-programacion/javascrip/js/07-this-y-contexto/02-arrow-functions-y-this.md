# Arrow Functions y `this`

Las **Arrow Functions** (funciones flecha), introducidas en ES6, se diferencian radicalmente de las funciones tradicionales en su manejo de `this`: **no tienen un `this` propio**. En su lugar, utilizan el valor de `this` del ámbito léxico (el lugar donde fueron definidas).

---

## El Concepto de `this` Léxico

Dentro de una función de flecha, `this` se resuelve como cualquier otra variable: buscando en el ámbito superior hasta encontrar un valor. Una vez definido el contexto en el momento de la creación, este **no puede cambiar**, incluso si usamos `call`, `apply` o `bind`.

```javascript
const usuario = {
  nombre: 'Ana',
  presentar: function() {
    // Aquí this es 'usuario'
    const saludoFlecha = () => {
      console.log(`Hola, soy ${this.nombre}`);
    };
    saludoFlecha();
  }
};

usuario.presentar(); // "Hola, soy Ana"
```

---

## Comportamiento en Métodos de Objetos

> [!WARNING]
> **No uses Arrow Functions como métodos de objetos** si necesitas acceder a otras propiedades del mismo objeto mediante `this`.

Como las funciones de flecha capturan el `this` del entorno donde se definen (a menudo el ámbito global), fallarán al intentar actuar como métodos:

```javascript
const perfil = {
  puntos: 100,
  sumar: () => {
    // ERROR: this no es 'perfil', es el objeto global o undefined
    this.puntos++; 
  }
};

perfil.sumar();
console.log(perfil.puntos); // Seguirá siendo 100
```

---

## Uso en Callbacks (Beneficios)

Donde las Arrow Functions realmente brillan es en los callbacks, ya que preservan de forma natural el contexto de la clase o función contenedora sin necesidad de hacks antiguos.

```javascript
class Temporizador {
  constructor() {
    this.segundos = 0;
  }

  iniciar() {
    setInterval(() => {
      // 'this' hereda correctamente el contexto de la instancia
      this.segundos++;
      console.log(this.segundos);
    }, 1000);
  }
}
```

> [!NOTE]
> Con una función tradicional, `this` dentro de `setInterval` apuntaría al objeto global, obligándonos a usar `.bind(this)` o guardar la referencia en otra variable.

---

## Comportamiento en Event Listeners

Si utilizas una función de flecha en un `addEventListener`, pierdes la referencia automática al elemento que disparó el evento (que suele estar en `this`).

```javascript
const btn = document.querySelector('#miBoton');

// Con función normal: this es el botón
btn.addEventListener('click', function() {
  this.classList.toggle('activo');
});

// Con Arrow Function: this es el contexto exterior (ej. window)
btn.addEventListener('click', (e) => {
  // Solución: Usar e.currentTarget o e.target
  e.currentTarget.classList.toggle('activo');
});
```

---

## Limitaciones Técnicas

> [!CAUTION]
> Debido a su naturaleza simplificada, las Arrow Functions tienen restricciones importantes:
> 1.  **No son constructoras:** No puedes usar `new` con ellas. Lanzarán un `TypeError`.
> 2.  **Sin `prototype`:** No tienen propiedad de prototipo.
> 3.  **Sin `arguments`:** No poseen el objeto `arguments` (puedes usar el parámetro Rest `...args` en su lugar).

---

## Resumen y Mejores Prácticas

| Característica | Función Tradicional | Arrow Function |
| :--- | :--- | :--- |
| **`this`** | Dinámico (cómo se llama) | Léxico (dónde se define) |
| **Constructor** | Sí (con `new`) | No |
| **Uso Ideal** | Métodos de objetos, prototipos | Callbacks, Promesas, Funcional |
| **Prototipo** | Tiene `prototype` | No tiene |

---
[Volver al Índice](../js-index.md)
