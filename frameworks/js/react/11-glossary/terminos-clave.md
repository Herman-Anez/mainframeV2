# Glosario de términos clave de React

## A

**Atomic Design** – Metodología de diseño de sistemas de componentes que divide la interfaz en átomos, moléculas, organismos, plantillas y páginas.

## B

**Batching** – Agrupación de múltiples actualizaciones de estado en un solo re‑render para mejorar el rendimiento. En React 18 es automático incluso dentro de promesas o `setTimeout`.

## C

**Children** – Prop especial (`props.children`) que permite pasar contenido anidado a un componente.

**Code Splitting** – División del código en varios paquetes (chunks) que se cargan bajo demanda, normalmente con `React.lazy` y `Suspense`.

**Componente** – Pieza reutilizable de UI que puede ser una función o una clase. Recibe `props` y devuelve JSX.

**Composición** – Principio de construir componentes complejos combinando otros más simples, en lugar de usar herencia.

**Concurrent Rendering** – Capacidad de React para preparar múltiples versiones de la UI de forma interrumpible, priorizando actualizaciones urgentes.

**Context API** – Sistema nativo de React para compartir datos globales sin necesidad de pasar props manualmente (evita props drilling).

**Controlled Component** – Componente de formulario cuyo valor está controlado por el estado de React (usando `value` y `onChange`).

**CSS Modules** – Técnica que encapsula CSS a nivel de componente generando nombres de clase únicos.

**Custom Hook** – Función JavaScript que comienza con `use` y puede llamar a otros hooks. Permite reutilizar lógica con estado.

## D

**Default Props** – Valores por defecto para las props de un componente (definidos con `defaultProps` o desestructuración).

**Diffing** – Algoritmo que compara dos árboles del Virtual DOM para calcular el conjunto mínimo de cambios necesarios.

## E

**Error Boundary** – Componente de clase que captura errores de JavaScript en el árbol hijo y muestra una UI de fallback.

**Evento sintético** – Wrapper de React sobre eventos nativos del navegador, que unifica las diferencias entre navegadores.

## F

**Fiber** – Nueva arquitectura de React (desde v16) que permite dividir el trabajo de renderizado en unidades y priorizarlas.

**Fragment** – Componente especial (`<>...</>` o `<React.Fragment>`) que agrupa elementos sin añadir nodos extra al DOM.

**forwardRef** – Función que permite pasar una `ref` a través de un componente funcional hacia un nodo DOM interno.

## H

**HOC (Higher-Order Component)** – Función que recibe un componente y devuelve un nuevo componente mejorado. Patrón de reutilización anterior a los hooks.

**Hook** – Función especial que permite usar estado y otras características de React en componentes funcionales (ej. `useState`, `useEffect`).

**Hydration** – Proceso en SSR donde React vuelve a renderizar la aplicación en el cliente para adjuntar manejadores de eventos al HTML generado en el servidor.

## J

**JSX** – Extensión de sintaxis que permite escribir HTML dentro de JavaScript. Se compila a `React.createElement`.

## K

**Key** – Atributo especial usado en listas para ayudar a React a identificar qué elementos han cambiado, se han añadido o eliminado.

## L

**Lazy Loading** – Carga diferida de componentes o módulos usando `React.lazy` y `Suspense`.

## M

**Memo** – `React.memo` es un HOC que evita re‑renderizados innecesarios si las props no han cambiado (comparación superficial).

## P

**Portal** – Mecanismo para renderizar un componente hijo en un nodo DOM diferente al del componente padre, manteniendo el contexto de React.

**PropTypes** – Librería para validar el tipo de las props durante el desarrollo (útil para detectar errores).

**Props** – Datos de solo lectura que se pasan de un componente padre a un hijo.

**Props Drilling** – Situación en la que una prop pasa por muchos componentes intermedios que no la usan, solo para llegar a uno profundo.

## R

**Reconciliación** – Algoritmo que React utiliza para actualizar el DOM real basándose en las diferencias entre los árboles del Virtual DOM.

**Ref** – Objeto mutable (con propiedad `.current`) que persiste durante todo el ciclo de vida del componente. Se usa para acceder directamente a elementos DOM o guardar valores que no deben causar re‑render.

**Render Prop** – Patrón donde un componente recibe una función como prop (generalmente `children` o `render`) que retorna JSX, permitiendo al padre definir el renderizado.

## S

**Server Component** – Componente que se ejecuta solo en el servidor, sin enviar JavaScript al cliente. Puede ser `async` y acceder directamente a bases de datos.

**SSR (Server Side Rendering)** – Técnica que renderiza la aplicación React en el servidor y envía HTML al cliente, mejorando el rendimiento inicial y el SEO.

**State** – Datos que un componente puede modificar a lo largo del tiempo. Su cambio provoca un re‑render.

**Styled Components** – Librería de CSS‑in‑JS que permite escribir estilos encapsulados a nivel de componente usando template literals.

**Suspense** – Componente que muestra un fallback mientras se cargan componentes o datos de forma asíncrona (usado con `React.lazy` o data fetching).

## T

**Tailwind CSS** – Framework de utilidades CSS que proporciona clases atómicas para maquetar directamente en el JSX.

**Transition** – Actualización de estado marcada como no urgente con `useTransition` o `startTransition`, permitiendo mantener la UI responsiva.

## U

**Uncontrolled Component** – Componente de formulario cuyo valor es manejado directamente por el DOM, no por el estado de React (se accede con `ref`).

## V

**Virtual DOM** – Representación liviana del DOM real en memoria, que React utiliza para optimizar las actualizaciones mediante diffing y reconciliación.