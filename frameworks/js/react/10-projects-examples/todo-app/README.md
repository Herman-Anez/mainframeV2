# ✅ Ejemplo: Todo App (Gestión de Estado Local)

Este proyecto práctico demuestra cómo construir una aplicación de lista de tareas funcional utilizando los conceptos básicos de React: estado, props y renderizado de listas.

---

## 🏗️ Arquitectura del Ejemplo

La aplicación se divide en componentes pequeños y especializados para maximizar la reutilización y la legibilidad.

| Componente | Responsabilidad |
| :--- | :--- |
| **`TodoApp`** | Componente principal que contiene el estado (`todos`) y las funciones de lógica. |
| **`TodoForm`** | Formulario controlado para capturar nuevas tareas. |
| **`TodoList`** | Encargado de iterar sobre el array de tareas y renderizar los items. |
| **`TodoItem`** | Representación visual de una sola tarea con acciones (completar/eliminar). |

---

## 🧠 Conceptos Aplicados

1.  **Elevación de Estado (Lifting State Up)**: El estado de los `todos` vive en el padre (`TodoApp`) para que tanto la lista como el formulario puedan interactuar con él.
2.  **Inmutabilidad**: Al añadir o eliminar tareas, usamos el spread operator `[...todos]` o `.filter()` para no mutar el estado original.
3.  **Persistencia**: Uso de `useEffect` para sincronizar la lista con `localStorage`.

---

## 🚀 Desafíos Sugeridos

*   **Filtros**: Añade botones para filtrar tareas por "Completadas", "Pendientes" o "Todas".
*   **Edición**: Implementa la capacidad de editar el texto de una tarea ya creada.
*   **Animaciones**: Usa CSS Transitions para que las tareas aparezcan y desaparezcan suavemente.

---

<div align="center">

[⬅️ Volver al Índice](../../README.md)

</div>
