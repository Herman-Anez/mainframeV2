# Testing Paralelo en Playwright

Playwright fue diseñado con la paralelización como prioridad de primer nivel, superando a Selenium Grid en simplicidad.

## Conceptos Fundamentales

### Modelo de Browser Context
En lugar de múltiples instancias de navegador, Playwright crea múltiples **contextos de navegador**, cada uno aislado (cookies, localStorage, sesiones). Crear un contexto es casi tan barato como una pestaña. Esto permite ejecutar cientos de pruebas en paralelo dentro del mismo proceso.

### Aislamiento Total
Cada *worker* puede tener su propio navegador o compartir uno, pero los contextos garantizan que las pruebas no se interfieran entre sí.

## Configuración

En `playwright.config.ts` se define el número de workers:

```typescript
export default defineConfig({
  workers: 'auto', // O un número específico como 4
});
```

Playwright lanza automáticamente múltiples *workers* (procesos) que ejecutan pruebas en paralelo.

## Capacidades de Escalabilidad

- **Distribución Automática**: Pruebas independientes en diferentes archivos se distribuyen automáticamente entre los workers.
- **Proyectos (Projects)**: Se pueden configurar diferentes proyectos para combinar navegador y viewport, y Playwright ejecutará todos en paralelo.
- **Sharding**: Para CI a gran escala, Playwright soporta *sharding* (dividir la suite entre múltiples máquinas) con un simple parámetro de línea de comandos.

> [!TIP]
> **Ventaja para SDET**: Reduce drásticamente el tiempo de ejecución de la suite completa, un habilitador clave de la integración continua (CI) real.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Codegen & Grabación](./Codegen-grabacion.md) | [Home](../../../index.md) | [Automatización API](../../API/index.md) |


