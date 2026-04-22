
📄 8-advanced/concurrent-mode.md
Concepto

Concurrent Mode (ahora llamado Concurrent Rendering en React 18+) es un conjunto de características que permiten a React preparar múltiples versiones de la UI al mismo tiempo, sin bloquear el hilo principal. Puede pausar, reanudar y priorizar el trabajo de renderizado.
Problema que resuelve

En React tradicional, el renderizado es síncrono y no interrumpible. Si un render es pesado, bloquea el hilo principal y la UI se vuelve no responsiva (eventos, animaciones, entradas de teclado se retrasan).
Características del Concurrent Rendering

1. Renderizado interrumpible

React puede empezar a renderizar un árbol, pausar si llega un evento de mayor prioridad (ej. click del usuario), manejar ese evento, y luego reanudar el render anterior.
2. Priorización de actualizaciones

Las actualizaciones se clasifican por urgencia:

- Urgentes (clicks, inputs): deben reflejarse inmediatamente.

- Transiciones (cambios de ruta, filtros): pueden mostrar feedback de carga sin bloquear.

1. Suspense en el servidor (streaming SSR)

Permite enviar HTML al cliente por partes, mostrando fallbacks mientras se cargan datos.
Cómo optar por Concurrent Rendering (React 18+)

No hay un "modo concurrente" que se active mágicamente. Se habilita usando nuevas APIs como createRoot en lugar de ReactDOM.render.

```jsx
// Antes (React 17)
ReactDOM.render(<App />, document.getElementById('root'));

// Ahora (React 18)
import { createRoot } from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

Con createRoot, el Concurrent Rendering está disponible automáticamente para ciertas características como useTransition y Suspense.
APIs que dependen de Concurrent Rendering

- useTransition

- useDeferredValue

- `<Suspense>` mejorado (para data fetching)

- startTransition

Cómo funciona internamente (simplificado)

React divide el trabajo de renderizado en unidades (fibers) que pueden ser ejecutadas en múltiples frames del navegador. Usa requestIdleCallback o MessageChannel para programar el trabajo en los momentos de inactividad.
Ejemplo de interrupción

```jsx
// Sin Concurrent Rendering: un render pesado bloquea el input
function App() {
  const [text, setText] = useState('');
  const [heavyList, setHeavyList] = useState([]);
  
  const handleChange = (e) => {
    setText(e.target.value);
    setHeavyList(computeHeavyList(e.target.value)); // bloquea
  };
  
  // Con Concurrent Rendering y useTransition:
  const [isPending, startTransition] = useTransition();
  const handleChangeConcurrent = (e) => {
    setText(e.target.value);
    startTransition(() => {
      setHeavyList(computeHeavyList(e.target.value));
    });
  };
}
```

Limitaciones

- Algunas librerías de terceros pueden no ser compatibles (deben usar useSyncExternalStore).

- No todas las actualizaciones pueden ser interrumpibles (las de contexto global, por ejemplo, pueden tener efectos secundarios).

Buenas prácticas

- Envuelve actualizaciones lentas con startTransition o useTransition.

- Usa useDeferredValue para valores que pueden quedar desactualizados temporalmente.

    Prepara tu código para que sea "interrumpible": evita efectos secundarios en el render (solo los reducers puros).
