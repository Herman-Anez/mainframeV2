# Pruebas SAST y DAST (Conceptos y Estrategia)

Estas pruebas cubren dos enfoques complementarios de seguridad que el SDET debe orquestar en el pipeline.

## SAST (Static Application Security Testing) – "Caja Blanca"

Analiza el código fuente o bytecode sin ejecutar la aplicación. Detecta patrones de vulnerabilidades (inyecciones, mal manejo de errores, configuraciones inseguras) desde las fases tempranas.

- **Herramientas**:
    - **SonarQube / SonarCloud**: Con reglas de seguridad OWASP, detecta fallos de seguridad en el código. Se integra en PR con quality gates.
    - **Snyk Code / Semgrep / Checkmarx**: Soluciones específicas de SAST.
    - **Linters de Seguridad**: `bandit` para Python, `eslint-plugin-security` para JS.

> [!TIP]
> El SDET colabora configurando los umbrales de calidad (ej. no permitir nuevos issues de severidad *Blocker*) y asegurándose de que el escaneo se ejecuta en CI como un paso más.

**Ventajas**: Feedback inmediato, no requiere despliegue, cubre todo el código.

## DAST (Dynamic Application Security Testing) – "Caja Negra"

Ataca la aplicación en ejecución, simulando a un atacante externo. Generalmente utiliza un proxy (ZAP, Burp Suite Enterprise) o escáneres especializados (Nikto).

Detecta vulnerabilidades en tiempo de ejecución: XSS, SQLi, CSRF, errores de configuración del servidor.

> [!IMPORTANT]
> El SDET lo integra usando herramientas como **OWASP ZAP** o **Burp Suite CI**. Se requiere un entorno de pruebas estable y no productivo (staging).

## Triángulo de Pruebas de Seguridad en DevOps

1. **SAST** en el IDE (pre-commit) y en el build CI (post-commit).
2. **Análisis de dependencias (SCA)**: `npm audit`, `Snyk`, `OWASP Dependency Check`. Detectar vulnerabilidades en librerías. El SDET lo incluye en el pipeline y rompe el build si hay vulnerabilidades críticas con fix disponible.
3. **DAST** sobre la aplicación desplegada en staging (diario o en PR).
4. **Pruebas de penetración manuales**: Realizadas por expertos externos, fuera del alcance del SDET pero aprovechando los datos de automatización.

## Pipeline Integrado de Seguridad

```yaml
stages:
  - build
  - sast
  - test
  - dast
```

O más granular, con herramientas como Snyk, SonarQube, ZAP. El SDET puede configurar que la etapa `dast` se ejecute después del despliegue automático en el namespace de testing (K8s).

## Métricas y Umbrales

Definir con el equipo de seguridad un número máximo de vulnerabilidades permitidas por nivel (High, Medium). Por ejemplo, bloqueante: `>0 High` en DAST o SAST, `>0 Critical` en SCA. Este gating educa y acelera la corrección.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Seguridad Index](./index.md) | [Home](../../../index.md) | [OWASP ZAP Automation](./OWASP-ZAP-automation.md) |

