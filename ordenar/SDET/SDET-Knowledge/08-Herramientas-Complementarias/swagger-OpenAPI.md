# 📖 Swagger / OpenAPI

OpenAPI Specification (antes Swagger) es un estándar para describir APIs RESTful. Para un SDET, una especificación OpenAPI es una fuente de verdad que permite automatizar pruebas de contrato, generar clientes de prueba y validar la consistencia de la implementación.

---

## 🏗️ Uso de Swagger UI y Swagger Editor

*   **Swagger UI:** Interfaz web interactiva que lee un archivo `openapi.yaml` y permite hacer peticiones a la API directamente desde el navegador. El SDET la usa para explorar rápidamente los endpoints y entender la estructura de las peticiones/respuestas antes de codificar las pruebas.
*   **Swagger Editor:** Herramienta web para editar y visualizar en vivo el YAML/JSON. Ayuda a revisar la especificación o incluso a escribir ejemplos que luego se usarán en las pruebas.

---

## 🛡️ Validación de implementación contra la especificación

El SDET configura pruebas que verifican que la API real cumple lo prometido en el contrato OpenAPI. Esto se puede hacer de varias formas:

### 1. Respuestas contra esquema JSON
Cada respuesta de un endpoint se valida contra el esquema definido en la especificación. Librerías como `openapi4j` (Java) o `openapi-schema-validator` (Python, Node) leen el archivo OpenAPI y permiten validar cuerpos y cabeceras.

```java
// Con openapi4j
OpenApi3 api = new OpenApi3Parser().parse(new File("api.yaml"), false);
SchemaValidator val = new SchemaValidator("openapi.yaml");
val.validate(resp.getBody(), "/users/{id}", "get", 200);
```

### 2. Pruebas de contrato basadas en OpenAPI
Herramientas como **Dredd** o **Schemathesis** toman el archivo OpenAPI y generan solicitudes automáticas (incluso con datos aleatorios) para probar que la API responde según lo documentado. El SDET las integra en el pipeline de CI para detectar inconsistencias rápidamente. `Schemathesis`, por ejemplo, ejecuta pruebas de fuzzing basadas en la especificación.

### 3. Comparación de documentación y realidad
En algunos entornos, se puede invertir el flujo: la prueba captura las peticiones/respuestas de la API real y las compara con la especificación, asegurando que no haya cambios no documentados.

---

## ⚙️ Generación de código de cliente de pruebas

A partir de un `openapi.yaml` se puede generar automáticamente un cliente HTTP tipado que el SDET utiliza en sus pruebas, eliminando la necesidad de construir manualmente URLs y payloads.

*   **OpenAPI Generator:** Herramienta CLI que genera clientes en Java, Python, TypeScript, etc.
    *   *Ejemplo:* `openapi-generator-cli generate -i api.yaml -g java -o ./client`.
*   **Funcionamiento:** El código generado incluye métodos como `getUserById(id)` que ya devuelven objetos deserializados. El SDET integra este cliente en el proyecto de pruebas, lo que acelera el desarrollo y reduce errores de tipeo en las rutas.
*   **Mantenimiento:** Las pruebas dependen de la especificación. Si la API cambia, se regenera el cliente y el compilador indicará qué pruebas necesitan actualizarse, garantizando que la suite esté siempre sincronizada con el contrato.

---

## 🚀 API-first y participación del SDET

En un enfoque API-first, el equipo escribe la especificación OpenAPI antes del código. El SDET puede:

1.  **Participar en la revisión** de la especificación para asegurar que es testeable (por ejemplo, que incluye IDs únicos, que las respuestas de error están estandarizadas).
2.  **Crear stubs del servidor** a partir de la especificación para que el equipo de frontend y los testers tengan un mock realista mientras se desarrolla el backend.
3.  **Automatizar pruebas de integración** contra el mock y luego, una vez el backend está listo, contra la implementación real sin cambiar los tests (solo cambiar la URL).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [⬅️ Inicio del Módulo](index.md) | [🏠 Inicio](../../index.md) | [Fiddler & Charles Proxy ➡️](fiddler-Charles-proxy.md) |
