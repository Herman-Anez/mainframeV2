

📄 8-advanced/forwardRef.md
Concepto

forwardRef es una función de React que permite pasar una ref desde un componente padre a un componente hijo, y específicamente a un nodo DOM dentro de ese hijo. Es necesaria porque por defecto las ref no se pasan automáticamente a través de componentes funcionales.
Problema que resuelve
jsx

// ❌ Esto no funciona: ref apunta al componente funcional, no al input interno
function InputComponent() {
  return <input type="text" />;
}

function Parent() {
  const inputRef = useRef();
  return <InputComponent ref={inputRef} />; // Error: las funciones no aceptan ref directamente
}

Solución con forwardRef
jsx

import { forwardRef } from 'react';

const InputComponent = forwardRef((props, ref) => {
  return <input {...props} ref={ref} />;
});

function Parent() {
  const inputRef = useRef();
  
  useEffect(() => {
    inputRef.current.focus(); // Ahora sí funciona
  }, []);
  
  return <InputComponent ref={inputRef} placeholder="Escribe..." />;
}

Uso con múltiples elementos internos

Si el componente tiene varios elementos, debes decidir a cuál asignar la ref:
jsx

const FormGroup = forwardRef(({ label, ...props }, ref) => {
  return (
    <div>
      <label>{label}</label>
      <input ref={ref} {...props} />
    </div>
  );
});

forwardRef con TypeScript
tsx

interface InputProps {
  placeholder: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
));

Combinación con useImperativeHandle

forwardRef solo expone el nodo DOM. Si quieres exponer métodos personalizados, combínalo con useImperativeHandle:
jsx

const CustomInput = forwardRef((props, ref) => {
  const inputRef = useRef();
  
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ''; },
    getValue: () => inputRef.current.value
  }));
  
  return <input ref={inputRef} {...props} />;
});

// Padre
const ref = useRef();
ref.current.focus();
ref.current.clear();

forwardRef con HOCs

Si un componente está envuelto en un HOC, necesitas forwardRef para pasar la ref a través del HOC.
jsx

function withLogger(WrappedComponent) {
  const WithLogger = forwardRef((props, ref) => {
    useEffect(() => console.log('montado'), []);
    return <WrappedComponent {...props} ref={ref} />;
  });
  return WithLogger;
}

const EnhancedInput = withLogger(InputComponent);

¿Cuándo usar forwardRef?

    Cuando creas bibliotecas de componentes reutilizables.

    Cuando necesitas acceso directo al DOM de un componente hijo (medir, enfocar, scroll).

    Para integrar con librerías de terceros que requieren una ref (ej. animaciones, mapas).

Buenas prácticas

    No abuses de forwardRef. La mayoría de las interacciones deben hacerse mediante props y estado.

    Documenta qué ref se expone (¿el elemento principal? ¿el input?).

    Si no necesitas exponer la ref, no uses forwardRef.

Alternativas

    Callback ref: se puede pasar como prop normal (elementRef) pero rompe la convención de React.

    Contexto: para casos donde múltiples elementos necesitan acceso, pero es más pesado.
