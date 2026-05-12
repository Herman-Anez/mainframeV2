# Diferencias entre roles (Profundización)

Es crucial no solo listar los roles, sino entender las intersecciones y cómo varían sus actividades diarias, responsabilidades y habilidades.

## Mapeo de responsabilidades típico

| Actividad | QA Manual | QA Automation Engineer | SDET |
| :--- | :--- | :--- | :--- |
| **Ejecutar casos de prueba manuales** | Principal | Ocasional (regresiones no automatizables) | Rara vez (solo exploración técnica) |
| **Automatizar scripts de pruebas existentes** | No | Principal (mantener suite) | Sí, pero diseña el framework, no solo scripts |
| **Diseñar frameworks desde cero** | No | Básico (puede extender) | Principal |
| **Programar componentes reusables (APIs, servicios)** | No | Poco | Avanzado |
| **Escribir pruebas unitarias/de integración del producto** | No | No | Colabora, establece estándares |
| **Participar en la arquitectura del sistema** | No | No | Sí (revisiones de diseño) |
| **Gestionar pipelines CI/CD (groovy, yaml)** | No | Básico (disparar jobs) | Completo: creación, optimización, paralelización |
| **Pruebas de rendimiento/seguridad** | No | Ejecuta scripts dados | Diseña los planes, crea los scripts y analiza resultados |
| **Revisar código del producto** | No | No | Sí (peer review) |
| **Mentorizar desarrolladores en testing** | No | Poco | Frecuente (cultura de calidad) |

## La falsa jerarquía

> [!IMPORTANT]
> Comúnmente se cree que **QA Manual → QA Automation → SDET** es una progresión natural, pero es engañoso. Un SDET puede provenir de desarrollo de software sin haber sido nunca tester manual.

La diferencia fundamental está en la mentalidad de ingeniería: un QA Automation Engineer a menudo se limita a traducir casos manuales a código; un SDET piensa en cómo las pruebas deben modelar el sistema bajo prueba, con principios de diseño de software.

## Caso práctico: migración de suite de pruebas

*   **QA Automation Engineer**: Toma 200 casos de prueba en TestRail, implementa uno a uno en Selenium, usa Page Object Model copiado de un tutorial. Si la UI cambia drásticamente, actualiza manualmente los selectores en cada script.
*   **SDET**: Analiza el sistema, identifica componentes reutilizables, diseña una capa de abstracción de UI con Screenplay o componentes web genéricos. Crea un DSL (lenguaje específico de dominio) para que los testers puedan escribir pruebas en lenguaje casi natural. Ante un cambio de UI, modifica solo la capa de localización y recompone los tests sin tocarlos. Además integra variables de entorno y ejecución paralela desde el inicio.

## Habilidades comparativas

*   **QA Manual**: Gran capacidad analítica, ojo para detalles, dominio de técnicas de prueba, empatía con el usuario.
*   **QA Automation Engineer**: Programación a nivel de scripting (orientado a procedimientos), manejo de selectores y herramientas, ejecución de suites.
*   **SDET**: Programación orientada a objetos/funcional avanzada, diseño de software, conocimiento de protocolos de red, bases de datos, sistemas operativos, CI/CD, a menudo nivel similar a un desarrollador backend.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [¿Qué es un SDET?](01-Que-es-SDET.md) | [Índice](01-Que-es-SDET.md) | [Pirámide de Testing](03-Piramide-testing.md) ⏩ |

