# Data Factories

Son clases o funciones que construyen objetos de dominio (entidades) con valores por defecto inteligentes, a menudo usando el patrón *Builder* y bibliotecas como *Faker* para generar datos realistas. Permiten que los tests obtengan datos listos para insertar en BD o enviar a una API.

## Principios de una buena Data Factory

- **Valores por defecto sensatos**: Cada campo requerido tiene un valor significativo. Por ejemplo, `UserFactory.build()` genera un usuario con email único, password estándar y nombre ficticio.
- **Anulaciones específicas**: Mediante métodos encadenables se sobreescriben solo los campos necesarios: `UserFactory.withRole("ADMIN").withEmail("admin@test.com").build()`.
- **Persistencia opcional**: La factory puede ofrecer `build()` (devuelve el objeto sin persistir) y `create()` (inserta en BD y devuelve el objeto).
- **Limpieza automática**: Registra los objetos creados y provee un método `cleanUp()` que los borra al finalizar el test (o en un hook `@AfterAll`).

## Implementación (Java + Builder + Faker)

```java
public class UserFactory {
    private static final Faker faker = new Faker();
    private static final List<User> created = new ArrayList<>();

    public static User build() {
        return User.builder()
            .name(faker.name().fullName())
            .email(faker.internet().emailAddress())
            .password("Pass1234!")
            .role("USER")
            .build();
    }

    public static User create(DataSource ds) {
        User user = build();
        // Lógica de inserción en BD con JdbcTemplate
        created.add(user);
        return user;
    }

    public static void cleanAll(DataSource ds) {
        // DELETE FROM users WHERE id IN (...)
        created.clear();
    }
}
```

**Uso en el test**:
```java
User user = UserFactory.create(dataSource);
// Ejecución de la prueba con el usuario creado
```

> [!NOTE]
> En `@AfterEach` o `@AfterAll`, se debe llamar a `UserFactory.cleanAll(...)` para mantener el entorno limpio, a menos que se use *rollback* de transacciones.

## Patrones Avanzados

- **Object Mother**: Similar a la Factory pero con métodos estáticos predefinidos como `createStandardOrder()` o `createOverdueOrder()`. Útil cuando hay combinaciones de objetos comunes.
- **Data-Driven con archivos**: Combinar fábricas con archivos JSON/YAML que definan conjuntos de datos para tests específicos.
- **Randomized Testing**: Usar *Faker* con aleatoriedad, pero con la posibilidad de fijar una semilla (`new Faker(new Random(12345))`) para garantizar reproducibilidad.

## Conexión con Ecosistemas

- **Java**: Herramientas como **DBUnit** o **Database Rider** permiten definir *datasets* XML/YAML.
- **Python**: **factory_boy** junto con SQLAlchemy o Django ORM.
- **Node.js**: **knex** seed files o **faker** combinado con scripts personalizados.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Seeds & Fixtures Index](./index.md) | [Home](../../index.md) | [Seeds y Migraciones](./Seeds%20y%20migraciones%20para%20testing.md) |