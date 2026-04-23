# 🕹️ Controlados vs No Controlados: Manejo de Datos

Este documento explora las dos formas principales en que los componentes de React pueden manejar los datos de entrada (inputs), determinando quién posee la "fuente de verdad" de la información.

---

## 🟢 Componentes Controlados (Recomendado)

En un componente controlado, **React es el dueño del estado**. El valor del input se define mediante una prop (`value`) y se actualiza a través de un manejador de eventos (`onChange`).

### 🚀 Ejemplo Básico

```jsx
function FormularioControlado() {
  const [nombre, setNombre] = useState('');

  return (
    <input 
      type="text"
      value={nombre} 
      onChange={(e) => setNombre(e.target.value)} 
    />
  );
}
```

### ✅ Cuándo usarlo

* **Validación en tiempo real**: Comprobar si el texto cumple requisitos mientras el usuario escribe.
* **Formato dinámico**: Aplicar máscaras (ej: formatos de teléfono o moneda) automáticamente.
* **Deshabilitación condicional**: Bloquear botones de envío si los campos no son válidos.

---

## 🟠 Componentes No Controlados

En estos componentes, el **DOM mantiene el estado interno**. React simplemente "consulta" el valor cuando lo necesita, generalmente usando una `ref`.

### 🚀 Ejemplo Básico

```jsx
function FormularioNoControlado() {
  const inputRef = useRef();
  
  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Valor actual: ${inputRef.current.value}`);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} defaultValue="Valor inicial" />
      <button type="submit">Enviar</button>
    </form>
  );
}
```

### ✅ Cuándo usarlo

* **Rendimiento Crítico**: Cuando tienes cientos de inputs y quieres evitar el re-renderizado constante.
* **Librerías externas**: Integración con plugins de JS que no son de React (ej: selectores de fecha complejos).
* **Archivos**: Los inputs de tipo `file` son **siempre** no controlados en React.

---

## ⚖️ Comparativa Directa

| Característica | Controlado | No Controlado |
| :--- | :--- | :--- |
| **Fuente de la Verdad** | Estado de React | DOM del Navegador |
| **Acceso al Valor** | Inmediato (State) | Diferido (Ref) |
| **Validación** | Sencilla e instantánea | Compleja (en el submit) |
| **Complejidad** | Más código | Menos código inicial |
| **Re-renders** | En cada pulsación | Solo cuando cambia el componente |

---

## Casos de uso

Controlado es mejor cuando:

* Necesitas validar o transformar la entrada en cada tecla.

* El campo depende de otros campos.

* Quieres habilitar/deshabilitar botones según el valor.

* Usas librerías de formularios (Formik, React Hook Form en modo controlado).

No controlado es mejor cuando:

* Formularios muy simples.

* Necesitas el mínimo re-renderizado posible.

* Integras con librerías no React (ej. jQuery datepicker).

* Usas React Hook Form en modo no controlado (por defecto).

--

## 🧩 Casos Especiales

### Checkboxes y Radios

Para estos elementos, la propiedad correcta es `checked` en lugar de `value`.

```jsx
const [acepta, setAcepta] = useState(false);
<input 
  type="checkbox" 
  checked={acepta} 
  onChange={(e) => setAcepta(e.target.checked)} 
/>
```

### ⚡ React Hook Form (El Enfoque Híbrido)

Librerías como **React Hook Form** utilizan componentes no controlados por debajo para maximizar el rendimiento, pero exponen una API que se siente controlada y facilita la validación.

```jsx
const { register, handleSubmit } = useForm();
// register() aplica la lógica de ref automáticamente
<input {...register('nombre')} />
```

---

## 💡 Buenas Prácticas

1. **Preferir Controlados**: Son más predecibles y fáciles de testear para la mayoría de los casos.
2. **No Mezclar**: Nunca pases `value` y un valor por defecto al mismo tiempo; React te mostrará una advertencia de "componente cambiando de no controlado a controlado".
3. **Default Values**: En componentes no controlados, usa `defaultValue` o `defaultChecked` para establecer el valor inicial sin tomar el control del estado.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
