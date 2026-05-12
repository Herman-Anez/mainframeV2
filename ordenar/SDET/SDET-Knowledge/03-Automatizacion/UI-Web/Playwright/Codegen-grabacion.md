Codegen-grabacion

Playwright viene con codegen, una herramienta de generación de código por interacción. El SDET puede usarla para acelerar la creación de localizadores o esqueleto de pruebas, no como sustituto de la ingeniería.

    Uso: npx playwright codegen https://example.com abre una ventana del navegador y un inspector. Cada clic o entrada de texto se convierte en código Playwright que se puede copiar directamente.

    Beneficios:

        Genera selectores resilientes (basados en roles de accesibilidad, texto, IDs) en lugar de XPaths frágiles.

        Captura aserciones básicas (como page.waitForSelector).

        Ayuda a explorar la estructura de la app rápidamente.

    Buenas prácticas: No confiar ciegamente; el código generado debe ser refactorizado en Page Objects y combinado con fixtures. También puede usarse para grabar flujos y luego parametrizarlos.