
# eventos.md

## Manejo de eventos en React

Los eventos se nombran en camelCase y se pasan una función (no un string):

```tsx

<button onClick={handleClick}>Click</button>
```

## Definir manejadores

```tsx
function MiComponente() {
  function handleClick(e) {
    e.preventDefault();  // Previene comportamiento por defecto
    console.log('Clicked');
  }
  return <button onClick={handleClick}>Click</button>;
}
```

## Diferencia con HTML nativo

- No se usa addEventListener, se declara directamente en JSX.

- El objeto e (evento sintético) es compatible con todos los navegadores.

## Paso de parámetros

```tsx
<button onClick={() => eliminarItem(id)}>Eliminar</button>
```

Cuidado: crear una nueva función en cada render puede afectar rendimiento. Para casos críticos, usa useCallback.

## Eventos comunes

- onClick, onChange, onSubmit, onMouseEnter, onFocus, onBlur, onKeyDown, etc.

## EveNtos en formularios

```tsx
const [texto, setTexto] = useState('');

function handleChange(e) {
  setTexto(e.target.value);
}
<input type="text" value={texto} onChange={handleChange} />
```

Esto se llama componente controlado.
e.preventDefault() y e.stopPropagation()

Funcionan igual que en DOM nativo.
Eventos personalizados

React no tiene eventos personalizados como Vue; se usan props callback.
Buenas prácticas

- No usar funciones flecha directamente en el render si afectan rendimiento (excepto componentes pequeños).

- Extraer manejadores fuera del JSX para claridad.
[back](../index.md)
