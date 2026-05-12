Dockerfiles para testing

Un Dockerfile define la imagen que contiene todas las dependencias necesarias para ejecutar las pruebas. El SDET lo crea para encapsular la suite de automatización y sus herramientas.

Ejemplo de Dockerfile para un proyecto Java + Selenium:
dockerfile

FROM maven:3.9-eclipse-temurin-17

# Instalar dependencias de sistema para navegadores headless
RUN apt-get update && apt-get install -y \
    wget gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chrome y ChromeDriver (usando script oficial)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Descargar ChromeDriver compatible (se puede automatizar con WebDriverManager en el código de test)

# Copiar el código de pruebas
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src

# Por defecto, ejecutar la suite completa
CMD ["mvn", "test", "-Denv=staging", "-Dheadless=true"]

Buenas prácticas para SDET:

    Multi-stage builds: Construir artefactos en una stage y copiar solo lo necesario a la imagen final, reduciendo tamaño y superficie de ataque.

    Ejecutar como non-root: crear un usuario tester con permisos limitados.

    Manejo de secretos: no incluir contraseñas en la imagen; pasarlas como variables de entorno en tiempo de ejecución (-e DB_PASS=$DB_PASS).

    Tagging: versionar las imágenes con el commit SHA o la versión de la suite, para auditar qué versión de pruebas se ejecutó.

Docker Compose para entornos de testing completos:
Un archivo docker-compose.test.yml puede levantar la aplicación bajo test, la base de datos, un mock de terceros, y el contenedor de pruebas, todo interconectado. El SDET lo usa para pruebas de integración que requieren todo el stack.
yaml

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

El comando docker-compose -f docker-compose.test.yml run tests ejecuta las pruebas y extrae los reportes al host. En CI esto se convierte en un paso simple.