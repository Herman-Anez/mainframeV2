Seeds y migraciones para testing

El término “seeds” a menudo se refiere a datos de referencia que pueblan la base de datos antes de la ejecución de pruebas (catálogos, tipos de cuenta). El SDET los gestiona con herramientas de migración.

Flyway / Liquibase:

    Se pueden aplicar migraciones que inserten datos de prueba en entornos de testing (V1__insert_categories.sql). Pero cuidado: estas migraciones solo deben ejecutarse en entornos no productivos, mediante perfiles de Spring o configuraciones condicionales.

    Alternativa: usar scripts SQL en la carpeta test/resources/db/testdata que se ejecutan antes de cada suite con @Sql annotations (Spring) o manualmente en setUp.

Estrategia de limpieza:

    Borrado selectivo al finalizar cada clase de test: Si se conocen los datos creados, se eliminan por ID.

    Borrado total y recreación de esquema: Para suites pequeñas, se puede recalcular toda la BD desde cero con Flyway/Liquibase y luego insertar seeds. Es más lento pero garantiza estado limpio.

    Base de datos por sesión de prueba: Usar Docker para crear una base de datos nueva y destruirla al final. Con Testcontainers (Java, Python, Node) esto es transparente: cada suite levanta un contenedor de DB, ejecuta migraciones y se detiene al acabar.

Ejemplo con Testcontainers (Java):
java

@Container
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
    .withDatabaseName("test")
    .withUsername("test")
    .withPassword("test");

@BeforeAll
static void init() {
    DataSource ds = DataSourceBuilder.create()
        .url(postgres.getJdbcUrl())
        .username(postgres.getUsername())
        .password(postgres.getPassword())
        .build();
    Flyway.configure().dataSource(ds).load().migrate();
    // Insertar seeds adicionales
}

Data Factories y paralelismo:
Cuando las pruebas se ejecutan en paralelo (TestNG con varios hilos, JUnit5 en paralelo), las fábricas deben manejar concurrencia. Estrategias:

    Cada hilo usa su propio conjunto de IDs u objetos (usando ThreadLocal para el listado de objetos creados).

    Asegurar que los valores únicos (email, username) generados por Faker no colisionen; usar UUID o marcas de tiempo.

    Aislar completamente los datos por worker: ejecutar cada worker contra una base de datos diferente o schemas separados.

Dominar la interacción con bases de datos, ya sean relacionales o NoSQL, y la creación sistemática de datos permite al SDET escribir pruebas robustas, rápidas y altamente fiables. La clave es tratar los datos como parte del código de prueba, aplicando las mismas buenas prácticas de diseño.

