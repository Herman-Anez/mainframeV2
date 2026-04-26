# 🧪 Expresiones Regulares (RegEx)
> **Diccionario y utilidades de patrones de búsqueda**

Colección de expresiones regulares útiles para el mantenimiento de este repositorio y tareas de desarrollo general.

---

## 🛠️ Patrones para Markdown

### 1. Bloques de código vacíos
Detecta bloques de código sin contenido.
```regex
^```(\S*)\s*\n\s*```$
```

### 2. Encabezados solitarios (#)
Detecta líneas que solo contienen el símbolo `#`.
```regex
^\s*#\s*$
```

---

## 🔍 Selecciones Específicas

| Patrón | Descripción |
| :--- | :--- |
| `(?<=^\s*)#.*` | Selecciona toda la línea que comienza con `#`. |
| `(?<=^\s*)#` | Selecciona solo el símbolo `#` al inicio. |
| `(?<=^\s*)#(?!\!)` | Selecciona `#` al inicio pero excluye los que van seguidos de `!` (útil para ignorar callouts de GitHub). |

---
[⬅️ Volver al Dashboard](../README.md)