
## Archivo: `03-excepciones-trycatch.md`

Estructura básica
```js
try {
  // código que puede lanzar una excepción
} catch (error) {
  // manejo del error
} finally {
  // se ejecuta siempre, haya o no error
}
```

    Si ocurre un error en try, la ejecución salta inmediatamente al bloque catch. Luego, pase lo que pase, se ejecuta finally.

    El objeto error en catch puede ser cualquier cosa lanzada, pero se recomienda que sea una instancia de Error o sus subclases.

    catch puede omitir el paréntesis y la variable si no se necesita la información del error (ES2019+): catch { ... }.

### Lanzar errores: throw
```js
throw new Error('Mensaje descriptivo');
throw new TypeError('valor inválido');
throw 'esto no es buena práctica'; // evítalo
```

El motor crea un objeto Error con información de pila de llamadas (stack trace).
Copy constructor: new Error(message)

    Error, TypeError, RangeError, SyntaxError, ReferenceError, URIError, EvalError.

    Se pueden crear errores personalizados extendiendo Error:

```js
class ValidationError extends Error {
  constructor(message, campo) {
    super(message);
    this.name = 'ValidationError';
    this.field = campo;
  }
}
throw new ValidationError('Campo requerido', 'email');
```

¿Qué sucede si no se captura un error?

El error se propaga hacia arriba en la pila de llamadas. Si llega al ámbito global sin ser capturado, el script se detiene y se muestra en consola (navegador) o se termina el proceso (Node.js, a menos que haya un listener de uncaughtException). Esto provoca una mala experiencia de usuario.
Finally y return

El bloque finally se ejecuta incluso si try o catch tienen una sentencia return. La única forma de evitarlo es un cierre forzado del proceso (ej. process.exit()) o un bucle infinito. Si finally también tiene un return, ese valor sobreescribe cualquier return anterior. Se recomienda que finally no devuelva valores.
Patrones de uso

    Capturar errores en operaciones de entrada/salida (fetch, lectura de archivos) y mostrar mensajes amigables.

    En entornos asíncronos con async/await, usar try/catch alrededor del await.

    En promesas, el equivalente es .catch().

    En frameworks frontend, a menudo se usan barreras globales de error (componentDidCatch en React, o manejadores de ventana).

### Ejemplo robusto
```js
async function getUsers() {
  try {
    const response = await fetch('/api/users');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fallo al obtener usuarios:', error.message);
    // Opcional: relanzar o devolver valor por defecto
    return [];
  } finally {
    console.log('Petición finalizada');
  }
}
```

