# Arrow Functions y `this`

Las **arrow functions** (funciones flecha) se diferencian radicalmente de las funciones normales en el manejo de `this`: **no tienen su propio `this`**. En lugar de eso, capturan el valor de `this` del ámbito léxico que las envuelve en el momento de su definición.

## No vinculan `this` propio

Dentro de una arrow function, `this` se resuelve exactamente igual que cualquier otra variable del ámbito exterior. Si la arrow se define en un ámbito donde `this` es un objeto, ese objeto será `this` dentro de la arrow, sin importar cómo se invoque.

```js
const obj = {
  nombre: 'Ana',
  saludar: function() {
    // this es obj
    const arrow = () => {
      console.log(this.nombre);
    };
    arrow();
  }
};

obj.saludar(); // Ana
```

### El riesgo de usarlas como métodos

Si definimos la arrow directamente como método del objeto, **NO** funcionará como esperamos, porque la arrow captura `this` del ámbito de definición (que podría ser global/undefined), no el objeto.

```js
const obj = {
  nombre: 'Error',
  saludar: () => {
    console.log(this.nombre); // undefined o error
  }
};

obj.saludar(); // No imprime 'Error'
```

> [!WARNING]
> No uses arrow functions como métodos de objetos si necesitas acceder a `this` del propio objeto.

---

## Ventajas en callbacks

Donde las arrows brillan es en callbacks y funciones anidadas, evitando la necesidad de `.bind()` o `var self = this`.

```js
function Temporizador() {
  this.segundos = 0;
  setInterval(() => {
    this.segundos++; // this se refiere a la instancia de Temporizador
  }, 1000);
}
```

> [!NOTE]
> Con una función normal, `this.segundos` estaría creando una propiedad en el objeto global o lanzando un error en modo estricto.

---

## Arrow functions y `addEventListener`

Si usas una arrow en `addEventListener`, `this` **NO** apuntará al elemento que disparó el evento, sino al `this` del ámbito exterior. Si necesitas el elemento, utiliza `event.currentTarget` o `event.target`.

```js
element.addEventListener('click', (e) => {
  console.log(this); // no es el elemento
  console.log(e.currentTarget); // el elemento
});
```

---

## Arrow functions y constructores

> [!CAUTION]
> Las arrows no pueden ser usadas con `new`. Carecen de propiedad `prototype` y lanzarán un `TypeError` si se intenta.

---

## Puntos a recordar

- **`this` es léxico:** Se define dónde se escribe la función, no cómo se llama.
- **Sin argumentos propios:** No tienen `arguments`, `super` ni `new.target` propios; los heredan del contexto contenedor.
- **Ideales para callbacks:** Son extremadamente útiles para preservar el contexto de `this` en callbacks, promesas y programación funcional.
- **No aptas para métodos:** No son adecuadas para métodos de objetos (salvo que el método no use `this`).
