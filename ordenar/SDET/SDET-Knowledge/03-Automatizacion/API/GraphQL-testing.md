# GraphQL Testing

GraphQL requiere un enfoque diferente: una sola URL, consultas flexibles y validación de esquema.

## Características de las Pruebas GraphQL

- **Peticiones**: Son siempre `POST` a `/graphql` con un *query* en el cuerpo y variables opcionales.
- **Códigos de Estado**: La respuesta casi siempre tiene código `200 OK`, incluso si hay errores funcionales. Se debe validar el campo `errors` en el JSON.
- **Validación de Estructura**: No basta con el *status*; se debe verificar que los datos vengan con los campos solicitados y validar los errores de negocio.

## Implementación

### Con REST Assured
Se puede enviar una cadena de consulta y validar usando `JsonPath`.

```java
String query = "{ user(id: 1) { name email } }";
given()
    .body(new GraphQLQuery(query))
.when()
    .post("/graphql")
.then()
    .body("data.user.name", equalTo("Juan"))
    .body("data.user.email", notNullValue());
```

### Herramientas Especializadas
Para un testing más especializado, se pueden usar clientes como `graphql-java-tools` o construir la carga útil manualmente para mayor control.

## Validación de Esquema e Introspección
Se puede obtener el esquema mediante introspección y validar las respuestas contra él, o utilizar pruebas de contrato para asegurar la compatibilidad.

> [!IMPORTANT]
> **Desafíos**: Manejo de variables, mutaciones y carga de archivos. El SDET debe entender la semántica de errores (errores de sistema vs. de negocio) para realizar aserciones correctas.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Postman & Newman](./Postman-Newman.md) | [Home](../../index.md) | [Contract Testing (Pact)](./Contract-testing-Pact.md) |