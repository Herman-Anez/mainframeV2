testing/jest.md



Jest es un framework de pruebas de JavaScript desarrollado por Facebook, muy popular para probar aplicaciones React. Incluye assertions, mocks, spies, cobertura y modo watch.
Instalación (en Create React App ya viene incluido)
```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```


Estructura básica de una prueba
```jsx
// suma.js
export function suma(a, b) { return a + b; }

// suma.test.js
import { suma } from './suma';

test('suma 1 + 2 es igual a 3', () => {
  expect(suma(1, 2)).toBe(3);
});
```


Matchers comunes
```jsx
expect(valor).toBe(3);           // igualdad estricta (Object.is)
expect(valor).toEqual({ a: 1 }); // igualdad profunda para objetos
expect(valor).toBeTruthy();      // true
expect(valor).toBeFalsy();       // false
expect(valor).toBeNull();
expect(valor).toBeDefined();
expect(valor).toContain('substring');
expect(array).toHaveLength(3);
expect(fn).toThrow(Error);
```


Pruebas asíncronas
```jsx
test('fetch devuelve datos', async () => {
  const data = await fetchData();
  expect(data).toEqual({ id: 1 });
});

// con resolves / rejects
expect(fetchData()).resolves.toEqual({ id: 1 });
```


Mocks y spies
```jsx
// Mock de función
const mockFn = jest.fn();
mockFn('arg');
expect(mockFn).toHaveBeenCalledWith('arg');
expect(mockFn).toHaveBeenCalledTimes(1);

// Mock de módulo
jest.mock('axios');
import axios from 'axios';
axios.get.mockResolvedValue({ data: { id: 1 } });
```


Cobertura de código
```bash
npm test -- --coverage
```


Configuración (para proyectos que no usan CRA)

```js
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  transform: { '^.+\\.(js|jsx)$': 'babel-jest' }
};
```

Pruebas de componentes React con Jest sola (sin Testing Library)

No es común, pero se puede usar react-test-renderer para snapshots.
```jsx
import renderer from 'react-test-renderer';
import MiComponente from './MiComponente';

test('snapshot', () => {
  const tree = renderer.create(<MiComponente />).toJSON();
  expect(tree).toMatchSnapshot();
});
```


Buenas prácticas

- Pruebas aisladas, sin dependencia entre ellas.

- Usa describe para agrupar pruebas relacionadas.

- Nombres descriptivos: 'debería mostrar el mensaje de error cuando falla'.

- No abuses de snapshots (se rompen fácilmente).
