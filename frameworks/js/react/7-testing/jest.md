# 🃏 Jest: El Framework de Pruebas Definitivo

**Jest** es un framework de pruebas de JavaScript enfocado en la simplicidad. Es el estándar de oro para aplicaciones de React, integrando todo lo necesario (assertions, mocks, spies, cobertura) en un solo paquete.

---

## 🚀 Configuración Inicial

Si usas **Create React App (CRA)**, Jest ya viene configurado. Para otros proyectos (como Vite), necesitas instalarlo:

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

---

## 🏗️ Anatomía de un Test

Los archivos de prueba suelen llevar la extensión `.test.js` o `.spec.js`.

```jsx
import { sumar } from './calculadora';

// describe: Agrupa pruebas relacionadas
describe('Módulo de Calculadora', () => {
  
  // test o it: Define una prueba individual
  test('debería sumar 1 + 2 y devolver 3', () => {
    // expect: La aserción que define el resultado esperado
    expect(sumar(1, 2)).toBe(3);
  });

});
```

---

## 🔍 Matchers (Comparadores) más Usados

Jest ofrece una gran variedad de "matchers" para verificar diferentes tipos de valores:

```javascript
expect(valor).toBe(10);           // Igualdad estricta (primitivos)
expect(valor).toEqual({ a: 1 });  // Igualdad profunda (objetos y arrays)
expect(valor).toBeTruthy();       // Verifica si es un valor "verdadero"
expect(valor).toContain('React'); // Verifica si un string o array contiene el valor
expect(array).toHaveLength(5);    // Verifica el tamaño de un array
expect(fn).toThrow(Error);        // Verifica si una función lanza un error
```

---

## ⚓ Mocks y Spies

Los **Mocks** permiten simular el comportamiento de funciones o módulos complejos (como llamadas a APIs) para aislar la unidad de código que se está probando.

### Simular una Función
```javascript
const miMock = jest.fn((x) => x + 10);

miMock(5);
expect(miMock).toHaveBeenCalledWith(5);
expect(miMock).toHaveReturnedWith(15);
```

### Simular un Módulo (ej: Axios)
```javascript
import axios from 'axios';
jest.mock('axios');

test('debería obtener datos de usuario', async () => {
  axios.get.mockResolvedValue({ data: { nombre: 'Ana' } });
  // ... resto del test
});
```

---

## 🛡️ Pruebas de Snapshots

Las pruebas de **Snapshot** capturan la estructura del componente y la guardan en un archivo. Si el componente cambia en el futuro, Jest te avisará.

```jsx
import renderer from 'react-test-renderer';

test('Renderiza correctamente el componente Botón', () => {
  const tree = renderer.create(<Button text="Enviar" />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

> [!WARNING]
> No abuses de los Snapshots. Son útiles para detectar cambios visuales inesperados, pero pueden volverse ruidosos si el componente cambia frecuentemente durante el desarrollo.

---

## 💡 Buenas Prácticas

1.  **Isolation**: Cada test debe ser independiente. Nunca dependas del resultado de una prueba anterior.
2.  **Mantenimiento**: Usa `describe` y `it` para que los reportes de error sean fáciles de leer (ej: `describe('Login', () => { it('should fail with wrong password', ... ) })`).
3.  **Cobertura**: Ejecuta `npm test -- --coverage` para ver qué porcentaje de tu código está realmente protegido por pruebas.
4.  **Watch Mode**: Usa `--watch` durante el desarrollo para que los tests se ejecuten automáticamente al guardar archivos.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
