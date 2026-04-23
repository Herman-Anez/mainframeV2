# 🤝 Reconciliación: El Algoritmo de Sincronización

La **Reconciliación** es el proceso por el cual React actualiza el DOM real para que coincida con el Virtual DOM. Es el algoritmo de "diferenciación" (diffing) que permite que React sea rápido al evitar actualizaciones innecesarias.

---

## 🏗️ El Algoritmo de Diffing

Debido a que comparar dos árboles completos tiene una complejidad de **O(n³)**, React utiliza un algoritmo heurístico con una complejidad de **O(n)** basado en dos suposiciones principales:

1.  **Tipos Diferentes**: Dos elementos de tipos diferentes producirán árboles distintos.
2.  **Identidad con Keys**: El desarrollador puede usar la prop `key` para indicar qué elementos son estables entre renderizados.

---

## 📏 Reglas del Algoritmo

### 1. Elementos de Diferente Tipo
Si los elementos raíz de una rama cambian de tipo (ej: de `<div>` a `<span>`), React destruye todo el árbol antiguo y construye el nuevo desde cero.

```jsx
// ❌ Counter se destruirá y perderá su estado interno
// Antes
<div><Counter /></div>

// Después
<span><Counter /></span>
```

### 2. Elementos del Mismo Tipo
Si el tipo de elemento es el mismo, React solo actualiza los atributos que han cambiado (como `className` o `id`) y luego procesa los hijos de forma recursiva.

### 3. Componentes del Mismo Tipo
Cuando un componente se actualiza, la instancia permanece igual para que el **estado se preserve** entre renderizados. React actualiza las props de la instancia y ejecuta el ciclo de vida correspondiente.

---

## 🔑 La Importancia de las Keys

Las `keys` permiten a React identificar elementos a través de múltiples renders. Son cruciales en el manejo de listas.

```jsx
// ❌ Ineficiente: Sin keys, React reconstruye los <li> si el orden cambia.
// ✅ Eficiente: Con keys, React simplemente reordena los nodos existentes.
<ul>
  <li key="user1">Ana</li>
  <li key="user2">Luis</li>
</ul>
```

> [!WARNING]
> Nunca uses el **índice del array** como `key` si la lista puede ser reordenada, filtrada o modificada. Esto causará bugs visuales y problemas de estado impredecibles.

---

## ⚡ React Fiber (Arquitectura Actual)

Desde la versión 16, React utiliza una nueva arquitectura llamada **Fiber**. A diferencia del algoritmo antiguo que era síncrono y recursivo, Fiber permite:
*   **Dividir el trabajo**: Segmentar la reconciliación en pequeñas unidades.
*   **Priorizar tareas**: Dar más importancia a animaciones o interacciones de usuario sobre actualizaciones de datos pesadas.
*   **Pausar y Reanudar**: Evita bloquear el hilo principal del navegador.

---

## 💡 Buenas Prácticas

1.  **Keys Estables**: Asegúrate de que las `keys` provengan de tus datos (ID de base de datos) y no cambien en cada renderizado.
2.  **Evitar Cambios de Estructura**: Mantener la jerarquía de componentes similar ayuda a React a reutilizar nodos del DOM.
3.  **Fragmentos**: Usa `<> ... </>` para agrupar elementos sin añadir nodos extra que el algoritmo deba procesar.
4.  **Reiniciar Estado**: Si intencionadamente quieres que un componente pierda su estado (ej: limpiar un formulario), cambia su `key`.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
