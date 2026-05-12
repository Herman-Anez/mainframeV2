# Codegen & Grabación

Playwright viene con `codegen`, una herramienta de generación de código por interacción. El SDET puede usarla para acelerar la creación de localizadores o esqueletos de pruebas, no como sustituto de la ingeniería.

## Uso

```bash
npx playwright codegen https://example.com
```

Abre una ventana del navegador y un inspector. Cada clic o entrada de texto se convierte en código Playwright que se puede copiar directamente.

## Beneficios

- **Selectores Resilientes**: Genera selectores basados en roles de accesibilidad, texto o IDs en lugar de XPaths frágiles.
- **Aserciones Básicas**: Captura aserciones automáticas (como `page.waitForSelector`).
- **Exploración Rápida**: Ayuda a entender la estructura de la app rápidamente.

> [!IMPORTANT]
> **Buenas prácticas**: No confiar ciegamente; el código generado debe ser refactorizado en Page Objects y combinado con *fixtures*. También puede usarse para grabar flujos y luego parametrizarlos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Playwright Index](./index.md) | [Home](../../../index.md) | [Testing Paralelo](./Testing-paralelo.md) |