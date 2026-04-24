
# Fundamentos de Arrays en JavaScript

Los arrays en JavaScript son objetos de alto nivel que permiten almacenar colecciones ordenadas de elementos. Internamente son objetos con claves numéricas (índices) y una propiedad `length` especial.

## Creación de Arrays

Existen diversas formas de inicializar un array, cada una con casos de uso específicos:

```javascript
const arr1 = [1, 2, 3];          // Literal (forma recomendada)
const arr2 = new Array(1, 2, 3); // Constructor (no recomendado con un solo argumento numérico)
const arr3 = Array.of(5);        // Crea [5] (soluciona la ambigüedad del constructor)
const arr4 = Array.from('hola'); // Convierte iterables o array-like en array: ['h','o','l','a']
```

> [!TIP]
> `Array.from()` es extremadamente útil para convertir estructuras como `NodeList` o el objeto `arguments` en arrays reales para usar sus métodos funcionales.

---

## Índices y Propiedad Length

*   **Índices:** Son enteros no negativos. Se accede mediante la notación de corchetes: `arr[indice]`.
*   **Propiedad `length`:** Representa siempre uno más que el mayor índice existente. No necesariamente coincide con el número real de elementos si existen "huecos".

### Manipulación de Length

Modificar `length` directamente trunca o extiende el array:
*   **Truncar:** Si se asigna un valor menor al actual, se eliminan permanentemente los elementos sobrantes.
*   **Extender:** Si se asigna un valor mayor, se crean huecos (`empty`), que se comportan como índices inexistentes.

```javascript
const a = [10, 20, 30];
a.length = 2;      // Resultado: [10, 20]
a.length = 5;      // Resultado: [10, 20, <3 empty items>]
console.log(a[3]); // undefined
```

---

## Arrays Dispersos (Sparse Arrays)

Los arrays pueden tener "agujeros" si se asignan índices no consecutivos.

```javascript
const sparse = [];
sparse[100] = 'a';
console.log(sparse.length); // 101
```

> [!WARNING]
> Los métodos que iteran (`forEach`, `map`, etc.) suelen ignorar los índices vacíos. Sin embargo, los bucles `for` tradicionales acceden a ellos devolviendo `undefined`. El operador `in` devuelve `false` para estos índices.

---

## Detección de Arrays

Dado que `typeof` devuelve `"object"`, la forma correcta de identificar un array es:

1.  **`Array.isArray(valor)` (ES5):** El método estándar y más recomendado.
2.  **`valor instanceof Array`:** Funciona en la mayoría de los casos, pero puede fallar en entornos con múltiples contextos (como iframes).

---

## Estrategias de Iteración

Existen múltiples formas de recorrer un array:

*   **`for` clásico:** `for (let i = 0; i < arr.length; i++)` - Ofrece control total sobre el índice, pero es más propenso a errores.
*   **`for...of`:** Recorre directamente los **valores**. Es la opción recomendada para legibilidad.
*   **`for...in`:** Recorre las **propiedades** (índices como strings). No se recomienda para arrays ya que puede incluir propiedades no numéricas.
*   **Métodos funcionales:** Como `forEach`, `map`, etc., que encapsulan la lógica de iteración.

---

## Comparación y Mutabilidad

Los arrays son objetos, por lo que dos arrays con el mismo contenido representan **referencias diferentes**. 

> [!IMPORTANT]
> La comparación `[] === []` siempre será `false`. Para comparar el contenido, se debe iterar manualmente o usar técnicas como `JSON.stringify()` (aunque esta última tiene limitaciones con ciertos tipos de datos).