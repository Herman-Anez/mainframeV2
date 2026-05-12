# Selenium Grid con Docker

Ejecutar pruebas UI en paralelo requiere una granja de navegadores eficiente. **Selenium Grid 4** se puede desplegar de forma robusta utilizando Docker, permitiendo escalar la ejecución según las necesidades de la suite.

## Despliegue con Docker Compose

```yaml
version: '3'
services:
  selenium-hub:
    image: selenium/hub:4.0
    container_name: selenium-hub
    ports:
      - "4444:4444"
  chrome:
    image: selenium/node-chrome:4.0
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
  firefox:
    image: selenium/node-firefox:4.0
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
```

El código de automatización se conecta al Hub mediante `RemoteWebDriver` apuntando a `http://localhost:4444`.

## Alternativas avanzadas

*   **Selenoid**: Utiliza contenedores efímeros por sesión, lo que ofrece mayor velocidad y menor consumo de recursos. Incluye una interfaz visual para ver las sesiones en vivo y grabar vídeos de las ejecuciones.
*   **Zalenium**: (Deprecado) Fue el precursor de Selenoid; hoy se recomienda migrar a Selenium Grid 4 o Selenoid.
*   **Moon**: Solución comercial para clústeres de Kubernetes con balanceo de carga y gestión de cuotas.

## Integración en CI/CD

En plataformas como GitHub Actions, se puede levantar el Grid como un servicio secundario:

```yaml
services:
  selenium:
    image: selenium/standalone-chrome
    ports:
      - 4444:4444
```

> [!NOTE]
> El SDET es responsable de configurar y escalar esta infraestructura. Si se requieren 50 o más sesiones concurrentes, la estrategia debe evolucionar hacia clústeres de **Docker Swarm** o **Kubernetes**.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Dockerfiles para testing](./Dockerfiles-testing.md) | [Home](../../../index.md) | [Kubernetes y Pruebas](../Kubernetes/index.md) |