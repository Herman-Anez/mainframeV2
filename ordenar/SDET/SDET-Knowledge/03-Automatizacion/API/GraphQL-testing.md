GraphQL-testing

GraphQL requiere un enfoque diferente: una sola URL, consultas flexibles y validación de esquema.

Características de las pruebas GraphQL:

    Las peticiones son POST a /graphql con un query en el body, variables opcionales.

    La respuesta siempre tiene código 200, pero puede contener errors o datos parciales.

    La validación no es solo de status, sino de estructura: que los datos vengan con los campos solicitados; también se verifican errores de negocio.

Herramientas y scripts:

    Con REST Assured: se puede enviar una cadena de consulta y validar usando JsonPath.
    java

    String query = "{ user(id: 1) { name email } }";
    given()
        .body(new GraphQLQuery(query))
    .when()
        .post("/graphql")
    .then()
        .body("data.user.name", equalTo("Juan"))
        .body("data.user.email", notNullValue());

    Para un testing más especializado, se pueden usar clientes como com.graphql-java-tools o simplemente construir la carga útil.

    Validación de esquema: Se puede obtener el esquema mediante introspección y validar las respuestas contra él, o usar pruebas de contrato.

Desafíos: Manejo de variables, mutaciones, carga de archivos. El SDET debe entender la semántica de errores (errores de sistema vs de negocio) para aserciones correctas.