
# Manejo de Excepciones: `try`, `catch` y `finally`

## Estructura Básica

Permite gestionar errores en tiempo de ejecución para evitar que la aplicación se detenga inesperadamente.

```javascript
try {
  // Código que puede lanzar una excepción
} catch (error) {
  // Manejo del error
} finally {
  // Se ejecuta siempre, haya o no error
}
```

*   **Flujo de Ejecución:** Si ocurre un error en el bloque `try`, la ejecución salta inmediatamente al bloque `catch`. Independientemente del resultado, el bloque `finally` se ejecutará al final.
*   **Objeto Error:** Aunque se puede lanzar cualquier valor, se recomienda encarecidamente lanzar instancias de `Error` o sus subclases para mantener la coherencia y obtener la pila de llamadas (*stack trace*).
*   **Catch Opcional (ES2019+):** Es posible omitir el parámetro del error si no se requiere su información: `catch { ... }`.

---

## Lanzar Errores: `throw`

Se utiliza para generar una excepción de forma manual.

```javascript
throw new Error('Mensaje descriptivo');
throw new TypeError('Valor inválido');
```

> [!WARNING]
> Evita lanzar tipos primitivos como cadenas de texto: `throw 'Error';`. Al hacerlo, pierdes el *stack trace* y dificultas la depuración profesional.

### Tipos de Errores Nativos
JavaScript incluye varios constructores de error especializados:
*   `Error`, `TypeError`, `RangeError`, `SyntaxError`, `ReferenceError`, `URIError`, `EvalError`.

### Errores Personalizados
Es posible extender la clase `Error` para crear excepciones específicas del dominio de tu aplicación.

```javascript
class ValidationError extends Error {
  constructor(message, campo) {
    super(message);
    this.name = 'ValidationError';
    this.field = campo;
  }
}

throw new ValidationError('Campo requerido', 'email');
```

---

## Propagación de Errores

Si un error no es capturado en el nivel actual, se propaga hacia arriba en la pila de llamadas (*call stack*).

> [!IMPORTANT]
> Si un error llega al ámbito global sin ser capturado:
> *   En el **navegador**: El script se detiene y el error se muestra en la consola.
> *   En **Node.js**: El proceso termina abruptamente (a menos que exista un *listener* de `uncaughtException`).
> Esto suele resultar en una pésima experiencia de usuario o inestabilidad en el servidor.

---

## `finally` y Sentencias `return`

El bloque `finally` tiene prioridad de ejecución. Incluso si existen sentencias `return` en `try` o `catch`, `finally` se ejecutará antes de que la función devuelva el valor.

> [!NOTE]
> Si el bloque `finally` contiene un `return`, este valor **sobrescribirá** cualquier valor devuelto previamente en `try` o `catch`. Por esta razón, se recomienda no devolver valores desde `finally`.

---

## Patrones de Uso y Buenas Prácticas

*   **E/S:** Capturar errores en operaciones de entrada/salida (como `fetch` o lectura de archivos).
*   **Async/Await:** Usar siempre `try/catch` envolviendo las llamadas con `await`.
*   **Promesas:** Utilizar el método `.catch()` para gestionar fallos en cadenas de promesas.
*   **Barreras de Error:** Implementar manejadores globales o "Error Boundaries" en frameworks modernos para una recuperación elegante.

### Ejemplo Robusto con `fetch`

```javascript
async function getUsers() {
  try {
    const response = await fetch('/api/users');
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Fallo al obtener usuarios:', error.message);
    return []; // Devolver un valor seguro por defecto
  } finally {
    console.log('Operación de obtención de usuarios finalizada.');
  }
}
```

---
