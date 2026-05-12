# SQL (Bases de Datos Relacionales)

El dominio de SQL permite al SDET verificar escenarios de negocio complejos directamente en la base de datos, asegurando que la persistencia de los datos sea correcta y eficiente.

## Temas de SQL

### 1. [Consultas Avanzadas](./Consultas-avanzadas.md)
JOINs, subconsultas, funciones de ventana (Window Functions) y CTEs para validaciones complejas.

### 2. [Procedimientos Almacenados](./Procedimientos-almacenados.md)
Estrategias para probar lógica de negocio encapsulada en la base de datos y validación de transacciones.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Bases de Datos Index](../index.md) | [Home](../../index.md) | [Consultas Avanzadas](./Consultas-avanzadas.md) |


Pruebas SAST y DAST (Conceptos y estrategia)

Estas pruebas cubren dos enfoques complementarios de seguridad que el SDET debe orquestar en el pipeline.

SAST (Static Application Security Testing) – "Caja blanca"

    Analiza el código fuente o bytecode sin ejecutar la aplicación. Detecta patrones de vulnerabilidades (inyecciones, mal manejo de errores, configuraciones inseguras) desde las fases tempranas.

    Herramientas:

        SonarQube / SonarCloud: Con reglas de seguridad OWASP, detecta fallos de seguridad en el código. Se integra en PR con quality gates.

        Snyk Code / Semgrep / Checkmarx: Soluciones específicas de SAST.

        Linters de seguridad: bandit para Python, eslint-plugin-security para JS.

    El SDET colabora configurando los umbrales de calidad (ej. no permitir nuevos issues de severidad Blocker) y asegurándose de que el escaneo se ejecuta en CI como un paso más.

    Ventajas: feedback inmediato, no requiere despliegue, cubre todo el código.

DAST (Dynamic Application Security Testing) – "Caja negra"

    Ataca la aplicación en ejecución, simulando a un atacante externo. Generalmente utiliza un proxy (ZAP, Burp Suite Enterprise) o escáneres especializados (Nikto).

    Detecta vulnerabilidades en tiempo de ejecución: XSS, SQLi, CSRF, errores de configuración del servidor.

    El SDET lo integra usando herramientas como OWASP ZAP (ver anterior) o Burp Suite CI.

    Se requiere un entorno de pruebas estable y no productivo. Por eso se lanza sobre entornos de staging.

Triángulo de pruebas de seguridad en DevOps:

    SAST en el IDE (pre-commit) y en el build CI (post-commit).

    Análisis de dependencias (SCA): npm audit, Snyk, OWASP Dependency Check. Detectar vulnerabilidades en librerías. El SDET lo incluye en el pipeline y rompe el build si hay vulnerabilidades críticas con fix disponible.

    DAST sobre la aplicación desplegada en staging (diario o en PR).

    Pruebas de penetración manuales: realizadas por expertos externos, fuera del alcance del SDET pero aprovechando los datos de automatización.

Pipeline integrado de seguridad:
yaml

stages:
  - build
  - sast
  - test
  - dast

O más granular, con herramientas como Snyk, SonarQube, ZAP. El SDET puede configurar que la etapa dast se ejecute después del despliegue automático en el namespace de testing (K8s).

Métricas y umbrales: Definir con el equipo de seguridad un número máximo de vulnerabilidades permitidas por nivel (High, Medium). Por ejemplo, bloqueante: >0 High en DAST o SAST, >0 Critical en SCA. Este gating educa y acelera la corrección.
