
# controlled-vs-uncontrolled.md

Diferencia entre cómo un componente maneja sus datos internamente (no controlado) vs. cómo React controla sus datos a través del estado (controlado).

## Componentes no controlados

- El DOM mantiene el estado (input, select, textarea).

- React solo lee el valor cuando es necesario (ej. onSubmit con ref).

- Se usa defaultValue en lugar de value.

```jsx
function FormularioNoControlado() {
  const inputRef = useRef();
  
  const handleSubmit = (e) => {
    e.preventDefault();
    alert(inputRef.current.value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} defaultValue="Texto inicial" />
      <button type="submit">Enviar</button>
    </form>
  );
}
```

## Componentes controlados

- React maneja el estado con useState.

- El valor del input se lee de state y se actualiza con onChange.

- El DOM es solo una representación del estado de React.

```jsx
function FormularioControlado() {
  const [valor, setValor] = useState('');
  
  return (
    <input 
      value={valor} 
      onChange={(e) => setValor(e.target.value)} 
    />
  );
}
```

Comparativa

|Característica|Controlado|No controlado|
|-|-|-|
|Fuente de la verdad|Estado de React|DOM|
|Validación en tiempo real|Fácil|Complejo|
|Formato dinámico (máscaras)|Fácil|Difícil|
|Rendimiento|Ligeramente peor (re-render)|Mejor|
|Simplicidad inicial|Más código|Menos código|
|Acceso a valores|Inmediato (estado)|Requiere ref|

## Casos de uso

Controlado es mejor cuando:

- Necesitas validar o transformar la entrada en cada tecla.

- El campo depende de otros campos.

- Quieres habilitar/deshabilitar botones según el valor.

- Usas librerías de formularios (Formik, React Hook Form en modo controlado).

No controlado es mejor cuando:

- Formularios muy simples.

- Necesitas el mínimo re-renderizado posible.

- Integras con librerías no React (ej. jQuery datepicker).

- Usas React Hook Form en modo no controlado (por defecto).

Inputs especiales

- Checkbox/radio controlado: checked={estado} onChange={handler}

- Select controlado: value={estado} onChange={handler}

```jsx
const [acepta, setAcepta] = useState(false);
<input type="checkbox" checked={acepta} onChange={(e) => setAcepta(e.target.checked)} />

React Hook Form (híbrido)

React Hook Form es mayormente no controlado por defecto (usa refs), pero puede ser controlado si se desea. Ofrece buen rendimiento.
```

```jsx
const { register, handleSubmit } = useForm();
<input {...register('nombre')} /> // no controlado
```

Buenas prácticas

- Prefiere controlado para formularios con validación o dependencias.

- Usa no controlado solo si el rendimiento es crítico o el formulario es trivial.

- No mezcles ambos en el mismo campo (o será de solo lectura).
