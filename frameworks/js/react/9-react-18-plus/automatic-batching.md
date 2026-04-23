# 📦 Automatic Batching: Eficiencia por Defecto

El **Automatic Batching** (Agrupamiento Automático) es una de las mejoras de rendimiento más significativas de React 18. Permite que React agrupe múltiples actualizaciones de estado en un solo re-renderizado, independientemente de dónde ocurran.

---

## 🤔 ¿Qué es el Batching?

El batching es cuando React agrupa varias llamadas a funciones de actualización de estado (`setState`) en un solo paso de procesamiento para mejorar el rendimiento. Esto evita que la interfaz se redibuje múltiples veces por cambios que ocurren al mismo tiempo.

---

## 🏗️ Antes de React 18 (Batching Limitado)

Anteriormente, React solo agrupaba actualizaciones dentro de los **manejadores de eventos de React** (como `onClick`). Las actualizaciones dentro de promesas, `setTimeout` o eventos nativos provocaban re-renderizados individuales.

```jsx
// ❌ Comportamiento antiguo (2 renders)
setTimeout(() => {
  setCount(c => c + 1); // Render 1
  setFlag(f => !f);     // Render 2
}, 100);
```

---

## 🚀 Con React 18 (Batching Total)

Con la llegada de `createRoot`, React ahora agrupa **todas** las actualizaciones de forma automática, sin importar el contexto.

```jsx
// ✅ Comportamiento moderno (1 solo render)
fetch('/api/data').then(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  setLoading(false);
  // React espera a que termine el callback y dispara un único render.
});
```

---

## ⚡ Cómo forzar un renderizado (`flushSync`)

En casos extremadamente raros donde necesites que el DOM se actualice inmediatamente después de un cambio de estado (por ejemplo, para medir un elemento justo después de un cambio), puedes usar `flushSync`.

```jsx
import { flushSync } from 'react-dom';

function handleClick() {
  flushSync(() => {
    setCount(c => c + 1); // Renderizado inmediato forzado
  });
  // El DOM ya está actualizado aquí
  flushSync(() => {
    setFlag(f => !f);     // Otro renderizado inmediato
  });
}
```

> [!CAUTION]
> Usa `flushSync` con mucha moderación. Puede degradar significativamente el rendimiento y romper las optimizaciones de concurrencia de React.

---

## 💡 Ventajas Clave

1.  **Menos Trabajo para la CPU**: Al reducir el número de renders, se ahorran ciclos de procesamiento.
2.  **Evita Estados Inconsistentes**: El usuario nunca llegará a ver un estado "intermedio" (ej: el contador actualizado pero la bandera de éxito aún en falso).
3.  **Código Limpio**: Ya no es necesario usar hacks o librerías externas para agrupar actualizaciones manuales.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
