# 💾 useState: Estado Local Básico

El **estado** representa los datos que pueden cambiar dentro de un componente a lo largo del tiempo. Cuando el estado cambia, React vuelve a renderizar el componente automáticamente para reflejar esos cambios en la UI.

---

## 🔌 Hook `useState`

Es la forma más sencilla de añadir reactividad a un componente funcional.

```jsx
import { useState } from 'react';

const Counter = () => {
  // [valor_actual, función_para_actualizar] = useState(valor_inicial)
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Has hecho clic {count} veces</p>
      <button onClick={() => setCount(count + 1)}>Incrementar</button>
    </div>
  );
};
```

---

## 🖇️ Actualización Segura

Cuando el nuevo estado depende del valor anterior, se recomienda usar una **función callback** dentro del setter para evitar inconsistencias por la naturaleza asíncrona de React.

> [!REDUNDANT]
> Esta información se repite detalladamente en [useState Avanzado](../2-hooks/useState.md).

```jsx
// ❌ Poco seguro en actualizaciones rápidas
setCount(count + 1);

// ✅ Forma correcta (Functional Update)
setCount(prevCount => prevCount + 1);
```

---

## 🧊 Inmutabilidad (Objetos y Arrays)

> [!CAUTION]
> React usa una comparación superficial para detectar cambios. Si mutas un objeto o array directamente, React no detectará el cambio y no re-renderizará.

> [!REDUNDANT]
> Los ejemplos de spread operator y manipulación de arrays están duplicados en [useState Avanzado](../2-hooks/useState.md).

### 📦 Con Objetos

```jsx
const [user, setUser] = useState({ name: 'Ana', age: 25 });

// ✅ Siempre crea una copia con spread
setUser({ ...user, age: 26 });
```

### 📋 Con Arrays

```jsx
const [items, setItems] = useState(['Manzana', 'Pera']);

// ✅ Agregar
setItems([...items, 'Plátano']);

// ✅ Eliminar
setItems(items.filter(item => item !== 'Pera'));
```

---

## 📏 Reglas y Buenas Prácticas

1. **Solo en el Nivel Superior**: No llames a `useState` dentro de bucles, condiciones o funciones anidadas.
2. **Estado Atómico**: Es mejor tener tres `useState` simples que uno gigante con un objeto complejo.
3. **No dupliques datos**: Si un valor puede calcularse a partir de otros (ej: `total = precio * cantidad`), no lo guardes en un estado. Calcúlalo durante el renderizado.

> [!REDUNDANT]
> Las reglas de hooks se repiten en casi todos los archivos de hooks y en la sección avanzada.

---

## ❓ ¿Cuándo usar estado?

- Datos que cambian por interacción del usuario (inputs, toggles).
- Datos que se cargan asincrónicamente (fetch).
- Valores que afectan el renderizado.

---

[⬅️ Volver al Índice](../README.md)

