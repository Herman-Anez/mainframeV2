Selenium Grid con Docker

Ejecutar pruebas UI en paralelo requiere una granja de navegadores. Selenium Grid se puede desplegar con Docker de forma oficial y robusta.

Selenium Grid 4 con Docker (hub + nodos):

    Imagen oficial: selenium/hub:4.0 y selenium/node-chrome:4.0, etc.

    Docker Compose clásico (Grid independiente):

yaml

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

    El test se conecta a http://localhost:4444 usando RemoteWebDriver y especificando capacidades del navegador.

Modo dinámico (Selenium Grid 4): No se necesita declarar los nodos; los nodos se registran automáticamente en el hub usando el mismo network. Se puede usar el docker-compose de la documentación oficial.

Alternativas avanzadas:

    Selenoid: contenedores efímeros por sesión, velocidad y menor consumo de recursos. Tiene UI para ver las sesiones y grabar vídeo.

    Zalenium (deprecado): fue precursor, hoy reemplazado por Selenoid/Selenium Grid 4.

    Moon (comercial): para clústeres Kubernetes, con balanceo y gestión de cuotas.

Integración en CI:
En GitHub Actions o Jenkins, se levanta el Grid como services o en un stage previo. Luego la suite usa RemoteWebDriver para ejecutar en remoto. Ejemplo con GitHub Actions services:
yaml

services:
  selenium:
    image: selenium/standalone-chrome
    ports:
      - 4444:4444

Luego el código apunta a http://localhost:4444/wd/hub.

El SDET configura la infraestructura de Grid y se encarga de la escalabilidad: si se necesitan 50 sesiones concurrentes, diseñará la estrategia de nodos y recursos en el clúster (Docker Swarm o Kubernetes).