# 🎨 CSS Modules: Estilos Encapsulados

Los **CSS Modules** permiten escribir CSS que tiene como ámbito automático el componente donde se importa. Esto resuelve el problema global del CSS nativo, evitando colisiones de nombres de clases.

---

## 🏗️ Configuración

Tanto **Vite** como **Create React App** soportan CSS Modules por defecto. Solo necesitas nombrar tus archivos con la extensión `.module.css` (o `.module.scss`).

---

## 🚀 Uso Básico

```css
/* Boton.module.css */
.boton {
  background: #3182ce;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
}

.primario {
  background: #2f855a;
}
```

```jsx
import styles from './Boton.module.css';

function Boton() {
  // Las clases se acceden como propiedades del objeto 'styles'
  return <button className={styles.boton}>Click aquí</button>;
}
```

---

## 🖇️ Manejo de Clases Múltiples y Props

Para combinar varias clases o usar lógica condicional, puedes usar plantillas de cadena (template strings):

```jsx
// Unión de clases estáticas
<button className={`${styles.boton} ${styles.primario}`}>
  Click
</button>

// Clases condicionales basadas en props
<button className={`${styles.boton} ${importante ? styles.urgente : ''}`}>
  Borrar
</button>
```

---

## ⚖️ Ventajas y Limitaciones

### ✅ Ventajas
*   **Encapsulamiento**: Los estilos no se filtran a otros componentes.
*   **Nombres Limpios**: Puedes usar nombres genéricos como `.container` o `.title` en todos tus archivos.
*   **Rendimiento**: Es CSS puro, procesado en tiempo de compilación.

### ❌ Desventajas
*   **Dinamicismo limitado**: No es tan potente como CSS-in-JS para temas altamente dinámicos.
*   **Verboso**: El acceso vía `styles.clase` puede hacer el JSX un poco más ruidoso.

---

## 🛠️ Alternativa: SCSS Modules

Si prefieres usar SASS/SCSS, simplemente instala la librería y usa la extensión `.module.scss`. Podrás usar anidación, variables y mixins con la misma seguridad de los módulos.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

