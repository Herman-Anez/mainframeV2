# Dockerfiles para testing

Un **Dockerfile** define la imagen que contiene todas las dependencias necesarias para ejecutar las pruebas. El SDET diseña estas imágenes para encapsular la suite de automatización, garantizando que se ejecute siempre bajo las mismas condiciones.

## Ejemplo: Java + Selenium en Docker

```dockerfile
FROM maven:3.9-eclipse-temurin-17

# Instalar dependencias de sistema para navegadores headless
RUN apt-get update && apt-get install -y \
    wget gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chrome y ChromeDriver
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Copiar el código de pruebas
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src

# Por defecto, ejecutar la suite completa en modo headless
CMD ["mvn", "test", "-Denv=staging", "-Dheadless=true"]
```

## Buenas prácticas para el SDET

*   **Multi-stage Builds**: Construir los artefactos en una etapa inicial y copiar solo lo estrictamente necesario a la imagen final para reducir el tamaño y mejorar la seguridad.
*   **Ejecución como non-root**: Crear un usuario específico (ej. `tester`) con permisos limitados dentro del contenedor.
*   **Manejo de Secretos**: Nunca incluir contraseñas en la imagen. Deben pasarse como variables de entorno en tiempo de ejecución (`-e DB_PASS=$DB_PASS`).
*   **Tagging**: Versionar las imágenes con el `commit SHA` o la versión de la suite para auditar qué versión exacta de las pruebas se ejecutó.

## Docker Compose para entornos completos

Un archivo `docker-compose.test.yml` permite levantar la aplicación bajo prueba, sus bases de datos y el contenedor de tests de forma interconectada.

```yaml
version: '3'
services:
  app:
    image: myapp:latest
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/test
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: test
  tests:
    build: .
    environment:
      APP_URL: http://app:8080
    depends_on:
      - app
      - db
    volumes:
      - ./reports:/app/reports
```

> [!TIP]
> El comando `docker-compose -f docker-compose.test.yml run tests` ejecuta las pruebas y mapea los reportes generados directamente a tu máquina host para su análisis.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Docker para entornos](./index.md) | [Home](../../../index.md) | [Selenium Grid con Docker](./Selenium-Grid-Docker.md) |