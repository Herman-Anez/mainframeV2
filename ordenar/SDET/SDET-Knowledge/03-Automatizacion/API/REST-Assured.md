REST Assured

Es la librería Java dominante para probar APIs REST. Usa un DSL fluido (given-when-then) que sigue el estilo BDD y facilita validar códigos de estado, cabeceras, cuerpos (JSON, XML) y tiempos.

Conceptos clave:

    Estructura: given() especifica cabeceras, parámetros, body. when() indica el método HTTP y la URL. then() realiza las validaciones.
    java

    given()
        .contentType(ContentType.JSON)
        .body(requestBody)
    .when()
        .post("/users")
    .then()
        .statusCode(201)
        .body("id", notNullValue())
        .body("name", equalTo("Juan"));

    Configuración base: RestAssured.baseURI = "http://api.example.com"; con RequestSpecification y ResponseSpecification reusables para autenticación, logging.

    Extracción de datos: Para encadenar pruebas, se extraen valores con extract().path("token") o usando JsonPath/GPath.

    Serialización/Deserialización: REST Assured integra Jackson/Gson para mapear automáticamente objetos Java a JSON y viceversa, facilitando pruebas tipadas.

    Autenticación: Soporta basic, OAuth2, form, digest. Se puede manejar de forma declarativa en la especificación de petición.

    Validación de esquemas: then().body(matchesJsonSchemaInClasspath("user-schema.json")).

    Manejo de logs: given().log().all() para depurar.

    Para SDET: Permite construir frameworks de prueba de API mantenibles usando especificaciones y herencia de configuraciones por entorno.