# REST Assured

Es la librería Java dominante para probar APIs REST. Usa un DSL fluido (*given-when-then*) que sigue el estilo BDD y facilita validar códigos de estado, cabeceras, cuerpos (JSON, XML) y tiempos.

## Conceptos Clave

### Estructura
`given()` especifica cabeceras, parámetros y cuerpo. `when()` indica el método HTTP y la URL. `then()` realiza las validaciones.

```java
given()
    .contentType(ContentType.JSON)
    .body(requestBody)
.when()
    .post("/users")
.then()
    .statusCode(201)
    .body("id", notNullValue())
    .body("name", equalTo("Juan"));
```

## Funcionalidades Avanzadas

- **Configuración Base**: `RestAssured.baseURI = "http://api.example.com"`. Permite usar `RequestSpecification` y `ResponseSpecification` reusables para autenticación y logging.
- **Extracción de Datos**: Para encadenar pruebas, se extraen valores con `extract().path("token")` o usando `JsonPath`/`GPath`.
- **Serialización**: Integra Jackson/Gson para mapear automáticamente objetos Java a JSON y viceversa, facilitando pruebas tipadas.
- **Autenticación**: Soporta *basic*, *OAuth2*, *form*, *digest*. Se puede manejar de forma declarativa.
- **Validación de Esquemas**: `then().body(matchesJsonSchemaInClasspath("user-schema.json"))`.
- **Logging**: `given().log().all()` para depurar peticiones y respuestas.

> [!TIP]
> **Para SDET**: Permite construir frameworks de prueba de API mantenibles usando especificaciones y herencia de configuraciones por entorno.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [API Index](./index.md) | [Home](../../index.md) | [Postman & Newman](./Postman-Newman.md) |