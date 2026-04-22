# Estado-useState.md

Estado local

El estado son datos que un componente puede modificar a lo largo del tiempo, causando un re-renderizado automático cuando cambian.
useState – Hook básico

```tsx
import { useState } from 'react';

function Contador() {
  const [contador, setContador] = useState(0);
  // contador = valor actual
  // setContador = función para actualizarlo
}
```

Reglas de useState

- Solo se puede usar en componentes funcionales o custom hooks.

- Siempre en el mismo orden (no dentro de condicionales o bucles).

- El argumento inicial solo se usa en la primera renderización.

Actualización del estado

```tsx
setContador(contador + 1);        // actualización directa
setContador(prev => prev + 1);    // forma segura cuando depende del valor anterior
```

## Estado con objetos o arrays

Debes crear una nueva copia (inmutabilidad):

```tsx
const [usuario, setUsuario] = useState({ nombre: 'Ana', edad: 30 });

// Correcto
setUsuario({ ...usuario, edad: 31 });

// Incorrecto (no provoca re-render)
usuario.edad = 31;
setUsuario(usuario);
```

Estado con arrays

```tsx
const [items, setItems] = useState([]);
setItems([...items, nuevoItem]);               // agregar
setItems(items.filter(i => i.id !== id));      // eliminar
setItems(items.map(i => i.id === id ? {...i, done: true} : i));
```

## Múltiples estados

Puedes usar varios useState o un useReducer si son muchas variables relacionadas.
¿Cuándo usar estado?

- Datos que cambian por interacción del usuario (inputs, toggles).

- Datos que se cargan asincrónicamente (fetch).

- Valores que afectan el renderizado.

No guardes en estado lo que se puede calcular

```tsx
// Mal
const [precio, setPrecio] = useState(10);
const [conIva, setConIva] = useState(12.1);
// Bien
const conIva = precio * 1.21;
```
[back](../index.md)
