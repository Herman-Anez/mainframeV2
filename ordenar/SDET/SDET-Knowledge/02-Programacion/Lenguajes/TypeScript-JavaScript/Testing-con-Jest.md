# Testing con Jest

Jest es el framework unitario/de integración por excelencia en proyectos React, Angular, Vue y Node.

## Características clave

*   **Configuración**: Viene preconfigurado en CRA (*Create React App*) y Vite. Soporta TypeScript con `ts-jest`. El SDET configura `jest.config.js` para definir raíces de pruebas, patrones de archivos, *coverage* y *mocks* globales.
*   **Matchers poderosos**: `toBe`, `toEqual` (comparación profunda), `toContain`, `toMatchObject`, `toThrow`. Jest extiende las posibilidades con `jest-extended`.
*   **Mocks y espías**: `jest.fn()` crea funciones simuladas. `jest.spyOn(object, method)` espía llamadas. Útil para simular módulos completos con `jest.mock('./module')`. En pruebas de componentes, se mockean APIs y librerías externas.
*   **Timers**: Con `jest.useFakeTimers()` se controlan `setTimeout` y `setInterval`. Permite simular el paso del tiempo y evitar esperas reales en pruebas de *timeouts* o animaciones.
*   **Pruebas de componentes UI**: Con *React Testing Library* (o *Vue Test Utils*) se monta el componente, se simulan eventos y se verifican salidas en el DOM, siguiendo el enfoque de testing centrado en el usuario.
*   **Snapshots**: Capturan la salida de un componente en un archivo para detectar cambios inesperados.
    > [!WARNING]
    > Un *snapshot* grande y opaco da falsa seguridad. Se deben usar con moderación y combinarse con aserciones específicas.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Asincronía](Asincronia.md) | [Índice](index.md) | [Programación](../../aux.md) ⏩ |