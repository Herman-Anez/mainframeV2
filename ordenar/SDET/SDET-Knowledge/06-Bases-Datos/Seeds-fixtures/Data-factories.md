Data Factories

Son clases o funciones que construyen objetos de dominio (entidades) con valores por defecto inteligentes, a menudo usando el patrón Builder y bibliotecas como Faker para datos realistas. Permiten que los tests obtengan datos listos para insertar en BD o enviar a una API.

Principios de una buena Data Factory:

    Valores por defecto sensatos: Cada campo requerido tiene un valor significativo para que la mayoría de las pruebas no tengan que especificarlo. Por ejemplo, UserFactory.build() genera un usuario con email único, password estándar, nombre ficticio.

    Anulaciones específicas: Mediante métodos encadenables se sobreescriben solo los campos necesarios: UserFactory.withRole("ADMIN").withEmail("admin@test.com").build().

    Persistencia opcional: La factory puede ofrecer build() (devuelve el objeto sin persistir) y create() (inserta en BD y devuelve el objeto).

    Limpieza automática: Registra los objetos creados en una lista y provee un método cleanUp() que los borra al finalizar el test (o en un hook @AfterAll). En transacciones, no suele ser necesario si se hace rollback.

Implementación con Builder y Faker (Java como referencia):
java

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
        // insertar en BD con JdbcTemplate
        // ...
        created.add(user);
        return user;
    }

    public static void cleanAll(DataSource ds) {
        // DELETE FROM users WHERE id IN (...)
        created.clear();
    }
}

En el test:
java

User user = UserFactory.create(dataSource);
// prueba con user

Y en @AfterEach o @AfterAll, llamar a UserFactory.cleanAll(...).

Patrones avanzados:

    Object Mother: Similar a Factory pero con métodos estáticos predefinidos como createStandardOrder(), createOverdueOrder(). Útil cuando hay combinaciones de objetos comunes en el dominio.

    Data-Driven con archivos: Combinar fábricas con archivos JSON/YAML que definan conjuntos de datos para un test específico. Por ejemplo, un archivo order-scenarios.json con varios pedidos en distintos estados y la factory los lee y los inserta.

    Randomized Testing: Usar Faker con aleatoriedad, pero con la posibilidad de fijar una semilla (faker = new Faker(new Random(12345))) para tener reproducibilidad.

Conexión con bases de datos:

    En proyectos Java, herramientas como DBUnit o Database Rider permiten definir datasets XML/YAML que limpian y pueblan tablas antes de cada prueba.

    En Python, factory_boy junto con SQLAlchemy o Django ORM proporciona la misma funcionalidad.

    En Node.js, knex seed files o faker combinado con un script seed.ts.