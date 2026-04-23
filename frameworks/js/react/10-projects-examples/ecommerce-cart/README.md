# 🛒 Ejemplo: Carrito de Compras (Context API)

Este ejemplo muestra cómo gestionar un estado global y persistente de una tienda online utilizando **Context API** y el hook **useReducer**.

---

## 🏗️ Arquitectura del Ejemplo

A diferencia de la Todo App, aquí centralizamos la lógica en un `Provider` para evitar el "prop drilling".

| Capa | Responsabilidad |
| :--- | :--- |
| **`CartContext`** | Definición del contexto y creación del Provider. |
| **`CartReducer`** | Lógica pura para manejar acciones: `ADD_TO_CART`, `REMOVE_ONE`, `CLEAR_CART`. |
| **`ProductList`** | Catálogo de productos que consume el contexto para añadir items. |
| **`CartModal`** | Vista detallada de los productos elegidos y el cálculo del total. |

---

## 🧠 Conceptos Aplicados

1.  **useReducer**: Ideal para manejar estados complejos donde una acción (añadir al carrito) implica lógica condicional (¿ya existe el producto? ¿sumamos cantidad?).
2.  **Context API**: Permite que cualquier componente (un botón en el sidebar o un icono en el header) acceda y modifique el carrito.
3.  **Derived State**: Calculamos el total de la compra y el conteo de items al vuelo durante el renderizado del contexto, asegurando la sincronía.

---

## 🚀 Desafíos Sugeridos

*   **Stock**: Implementa un límite de unidades por producto.
*   **Cupones**: Crea un sistema de descuentos que se aplique al total.
*   **Optimización**: Usa `useMemo` en el valor del Provider para evitar re-renderizados innecesarios del catálogo al cambiar el carrito.

---

<div align="center">

[⬅️ Volver al Índice](../../README.md)

</div>
