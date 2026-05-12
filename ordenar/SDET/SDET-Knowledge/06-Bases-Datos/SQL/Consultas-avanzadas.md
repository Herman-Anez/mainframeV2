# Consultas Avanzadas en SQL

Las consultas avanzadas permiten verificar escenarios de negocio complejos directamente en la base de datos. Para el SDET, esto significa poder validar que un pedido con sus líneas, pagos y direcciones se ha insertado correctamente sin tener que recorrer múltiples pantallas o endpoints.

## Tipos de Consultas y Validaciones

### 1. JOINs (INNER, LEFT, RIGHT, FULL, CROSS, SELF)
- **INNER JOIN**: Validar relaciones obligatorias. P.ej., comprobar que un usuario existe en `users` y tiene un perfil en `profiles`.
- **LEFT JOIN**: Útil para verificar integridad referencial. Detectar registros huérfanos:
  ```sql
  SELECT u.id FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE o.id IS NULL;
  ```
- **SELF JOIN**: Analizar jerarquías, como un empleado y su supervisor.
- **FULL OUTER JOIN**: Para contrastar dos fuentes de datos (p.ej., comparar una tabla de staging con la de producción).

> [!TIP]
> En automatización, se lanza un `SELECT ... JOIN ... WHERE ...` tras una operación de API y se aserta con `Assert.assertEquals(1, resultSet.size())` o iterando el `ResultSet`.

### 2. Subconsultas (Subqueries)
- **En WHERE**: Filtrar por valores agregados. Ejemplo: validar que el último pedido de un usuario tiene estado 'PAID'.
  ```sql
  SELECT * FROM orders o
  WHERE o.id = (SELECT MAX(id) FROM orders WHERE user_id = 123)
  AND o.status = 'PAID';
  ```
- **En FROM**: Tratar el resultado de una subconsulta como tabla temporal. Muy útil en pruebas para construir datos sobre la marcha.
- **En SELECT como columna**: Útil para enriquecer el resultado a verificar.

### 3. Window Functions (Funciones de Ventana)
- **Funciones**: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()`.
- **Ejemplo**: Comprobar la secuencia correcta de estados de un pedido (creado -> pagado -> enviado) usando `LAG(status) OVER (PARTITION BY order_id ORDER BY timestamp)`. El SDET puede afirmar que cada estado es el siguiente lógico comparando con el anterior.

### 4. CTEs (Common Table Expressions) – WITH
Mejoran la legibilidad. Se pueden encadenar múltiples CTEs para construir un resultado paso a paso y luego la consulta final.
```sql
WITH paid_orders AS (
  SELECT user_id, total FROM orders WHERE status = 'PAID'
),
user_totals AS (
  SELECT u.id, SUM(po.total) as total_paid
  FROM users u LEFT JOIN paid_orders po ON u.id = po.user_id
  GROUP BY u.id
)
SELECT * FROM user_totals WHERE total_paid > 1000;
```

> [!NOTE]
> El SDET usa CTEs para encapsular la lógica de verificación, haciendo las pruebas SQL autoexplicativas y fáciles de mantener.

### 5. Agregaciones y Filtrado (HAVING, GROUP BY)
- **GROUP BY** con funciones como `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- **HAVING** filtra después de agrupar.
- **Ejemplo**: Tras una importación de datos, verificar que la cantidad total de registros insertados por lote coincide con el fichero fuente.

### 6. Consultas Recursivas
Para estructuras de árbol. Verificar que al eliminar un nodo padre se eliminan sus hijos, mediante un CTE recursivo que compruebe que no existen descendientes.

## Integración en el Código de Prueba

- **Conexión**: JDBC en Java, `pyodbc`/`psycopg2` en Python, `knex` o `pg` en Node.
- **Utilidades**: El SDET crea una clase de utilidad de base de datos que encapsula `DataSource` y ofrece métodos como `executeQuery(String sql)` devolviendo `List<Map<String,Object>>` o `ResultSet` para aserciones.

### Ejemplo de Método Reutilizable (Java)
```java
public List<Map<String, Object>> getRows(String sql, Object... params) {
    return jdbcTemplate.queryForList(sql, params);
}
```
**Uso en la prueba**:
```java
assertThat(db.getRows("SELECT status FROM orders WHERE id=?", orderId), hasEntry("status", "PAID"));
```

> [!IMPORTANT]
> **Transacciones y aislamiento**: Las pruebas de BD deben ser atómicas. El SDET configura el framework para que cada prueba comience una transacción y haga rollback al final (Spring TestContext). Así se evita la contaminación entre pruebas.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [SQL Index](./index.md) | [Home](../../index.md) | [Procedimientos Almacenados](./Procedimientos-almacenados.md) |