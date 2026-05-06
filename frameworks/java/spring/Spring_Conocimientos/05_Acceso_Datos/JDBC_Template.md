# Acceso_Datos/JDBC_Template.md
El dolor que resuelve: JDBC crudo

JDBC es potente pero requiere código repetitivo: abrir conexiones, preparar sentencias, recorrer ResultSet, cerrar recursos en finally anidados y manejar la omnipresente SQLException. Spring elimina esa fricción con JdbcTemplate, que sigue el patrón Template Method: el recurso se abre y cierra automáticamente, y tu código se centra en la lógica SQL y el mapeo.
Configuración del DataSource

Todo comienza con un DataSource. Spring Boot lo autoconfigura a partir de las propiedades spring.datasource.*. Si no hay propiedades, intenta una base de datos embebida (H2) si encuentra el driver. En configuración manual:
java

@Bean
public DataSource dataSource() {
    HikariConfig config = new HikariConfig();
    config.setJdbcUrl("jdbc:mysql://localhost/midb");
    config.setUsername("user");
    config.setPassword("pass");
    return new HikariDataSource(config);
}

@Bean
public JdbcTemplate jdbcTemplate(DataSource ds) {
    return new JdbcTemplate(ds);
}

Spring Boot incluye HikariCP como pool por defecto, el más rápido.
Operaciones básicas con JdbcTemplate

Una vez inyectado JdbcTemplate, los métodos principales son:

    queryForObject(String sql, Class<T> tipo, Object... args) : para un solo valor (ej. Integer count). Lanza EmptyResultDataAccessException si no hay resultados.

    queryForList(String sql, Class<T> tipo, Object... args) : lista de valores únicos.

    query(String sql, RowMapper<T> rowMapper, Object... args) : lista de objetos mapeados.

    queryForMap(String sql, Object... args) : un solo registro como Map<String,Object>.

    update(String sql, Object... args) : INSERT, UPDATE, DELETE. Devuelve el número de filas afectadas.

    batchUpdate(String sql, List<Object[]> batchArgs) : múltiples actualizaciones en lote.

    execute(String sql) : para DDL o ejecución genérica.

RowMapper: el puente entre ResultSet y objetos

Interfaz funcional clave:
java

public class ProductoRowMapper implements RowMapper<Producto> {
    @Override
    public Producto mapRow(ResultSet rs, int rowNum) throws SQLException {
        Producto p = new Producto();
        p.setId(rs.getLong("id"));
        p.setNombre(rs.getString("nombre"));
        p.setPrecio(rs.getBigDecimal("precio"));
        return p;
    }
}

Se puede usar lambda: (rs, rowNum) -> new Producto(...). Spring proporciona BeanPropertyRowMapper<Producto>(Producto.class) que mapea por nombres de columna (si coinciden), pero tiene limitaciones (no soporta conversiones complejas, ligeramente más lento).
Ejemplo de consulta con parámetros
java

public Optional<Producto> findById(Long id) {
    try {
        Producto p = jdbcTemplate.queryForObject(
            "SELECT id, nombre, precio FROM productos WHERE id = ?",
            new ProductoRowMapper(), id);
        return Optional.of(p);
    } catch (EmptyResultDataAccessException e) {
        return Optional.empty();
    }
}

NamedParameterJdbcTemplate

En lugar de ?, puedes usar parámetros con nombre (:id). Requiere un NamedParameterJdbcTemplate, que internamente delega en el JdbcTemplate estándar.
java

String sql = "SELECT * FROM productos WHERE nombre = :nombre AND precio < :precio";
Map<String, Object> params = Map.of("nombre", "Teclado", "precio", new BigDecimal(100));
List<Producto> productos = namedJdbcTemplate.query(sql, params, new ProductoRowMapper());

Muy práctico cuando hay muchos parámetros y mejora la legibilidad.
ResultSetExtractor y RowCallbackHandler

    ResultSetExtractor: para procesar el ResultSet completo dentro de una sola callback (ej. construir estructura jerárquica a partir de múltiples filas). Se usa con query(sql, ResultSetExtractor).

    RowCallbackHandler: para procesar fila a fila sin devolver nada (no acumula resultados). Ideal para volcados o streamings.

Gestión de excepciones

JDBC lanza SQLException y sus derivados. JdbcTemplate traduce automáticamente estas excepciones a la jerarquía de DataAccessException de Spring, que son unchecked y más informativas: DataIntegrityViolationException, DuplicateKeyException, BadSqlGrammarException, etc. Esta traducción se realiza mediante un SQLExceptionTranslator configurable.
Operaciones por lotes (batch)

Para insertar miles de registros eficientemente:
java

List<Object[]> batch = productos.stream()
    .map(p -> new Object[]{p.getNombre(), p.getPrecio()})
    .collect(toList());
jdbcTemplate.batchUpdate("INSERT INTO productos (nombre, precio) VALUES (?,?)", batch);

batchUpdate permite también indicar el tamaño de lote y manejar devoluciones de claves generadas mediante PreparedStatement con KeyHolder.
Recuperación de claves generadas
java

KeyHolder keyHolder = new GeneratedKeyHolder();
jdbcTemplate.update(connection -> {
    PreparedStatement ps = connection.prepareStatement(
        "INSERT INTO productos (nombre, precio) VALUES (?,?)", 
        Statement.RETURN_GENERATED_KEYS);
    ps.setString(1, p.getNombre());
    ps.setBigDecimal(2, p.getPrecio());
    return ps;
}, keyHolder);
Long nuevoId = keyHolder.getKey().longValue();

Llamada a stored procedures y funciones

Se puede usar JdbcTemplate.call(...) con CallableStatementCreator y CallableStatementCallback, pero hay alternativas más modernas como SimpleJdbcCall:
java

SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
    .withProcedureName("actualizar_stock")
    .declareParameters(
        new SqlParameter("p_id", Types.INTEGER),
        new SqlParameter("p_cantidad", Types.INTEGER));
Map<String, Object> inParams = Map.of("p_id", id, "p_cantidad", cantidad);
jdbcCall.execute(inParams);

Sin embargo, Spring Data JPA o JDBC simplifican aún más esto.
Cuándo usar JdbcTemplate frente a JPA

    Si necesitas control absoluto sobre el SQL y rendimiento máximo.

    En aplicaciones pequeñas o consultas muy específicas donde un ORM es excesivo.

    Cuando el modelo de datos no encaja bien con entidades JPA.

    Para migraciones o tareas batch.

Spring ofrece también Spring Data JDBC, que combina el estilo de repositorios de Spring Data con JdbcTemplate pero sin JPA ni mapeo complejo.
