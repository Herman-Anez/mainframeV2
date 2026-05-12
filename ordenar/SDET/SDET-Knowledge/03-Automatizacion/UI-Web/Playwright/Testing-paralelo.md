Testing-paralelo

Playwright fue diseñado con la paralelización como prioridad de primer nivel, superando a Selenium Grid en simplicidad.

    Modelo de Browser Context: En lugar de múltiples instancias de navegador, Playwright crea múltiples contextos de navegador, cada uno aislado (cookies, localStorage, sesiones). Crear un contexto es casi tan barato como una pestaña. Esto permite ejecutar cientos de pruebas en paralelo dentro del mismo proceso.

    Configuración: En playwright.config.ts se define workers: 4 (o 'auto'). Playwright lanza automáticamente múltiples workers (procesos) que ejecutan pruebas en paralelo.

    Aislamiento total: Cada worker puede tener su propio navegador o compartir uno, pero los contextos garantizan que las pruebas no se interfieran.

    Ejemplos de paralelización:

        Pruebas independientes en diferentes archivos se distribuyen automáticamente.

        Se pueden configurar diferentes proyectos (projects) para combinar navegador y viewport, y Playwright ejecutará todos en paralelo.

    Sharding: Para CI a gran escala, Playwright soporta sharding (dividir la suite entre múltiples máquinas) con un simple parámetro.

    Ventaja para SDET: Reduce drásticamente el tiempo de ejecución de la suite completa, un habilitador clave de la integración continua real.

