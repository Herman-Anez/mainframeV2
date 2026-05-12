# Procedimientos Almacenados

Muchas aplicaciones encapsulan lógica de negocio crítica en *stored procedures* (SP). El SDET a veces debe probarlos directamente, validando las transformaciones y el manejo de errores desde la capa de datos.

## ¿Qué probar en un SP?

1.  **Lógica de negocio**: SP que calcula descuentos, asigna estados, realiza movimientos entre cuentas.
2.  **Manejo de parámetros**: Probar con valores válidos, límites, nulos y tipos incorrectos (aunque el driver maneje errores).
3.  **Salidas**: Parámetros de salida (`OUT`), códigos de retorno y conjuntos de resultados múltiples.
4.  **Transacciones y rollback**: Verificar que, ante un error en el SP, no se persisten cambios parciales.
5.  **Rendimiento**: Comparar tiempos de ejecución para detectar planes de ejecución degradados.

## Estrategia de Pruebas de SP

- **Entorno aislado**: Usar una base de datos con esquema de pruebas o un contenedor Docker (PostgreSQL/MySQL) que se crea al inicio de la suite.
- **Preparación de datos**: Insertar datos conocidos mediante scripts SQL o *data factories*.
- **Ejecución**: Llamar al SP mediante JDBC `CallableStatement` o `jdbcTemplate.call(...)`.
- **Validación**: Verificar los parámetros `OUT`, el resultado directo y el estado de las tablas tras la ejecución.

### Ejemplo de Implementación (Java)
```java
SimpleJdbcCall call = new SimpleJdbcCall(dataSource)
    .withProcedureName("transfer_funds")
    .declareParameters(
        new SqlParameter("from_account", Types.INTEGER),
        new SqlParameter("to_account", Types.INTEGER),
        new SqlParameter("amount", Types.DECIMAL),
        new SqlOutParameter("new_balance", Types.DECIMAL)
    );

Map<String, Object> result = call.execute(1, 2, new BigDecimal("100.00"));
assertThat(result.get("new_balance"), comparesEqualTo(new BigDecimal("900.00")));
// Además, validar con SELECT que el movimiento se registró en tabla 'transactions'.
```

> [!IMPORTANT]
> **Manejo de excepciones**: Si el SP lanza un error de negocio (p.ej., "saldo insuficiente"), se puede capturar con `assertThrows(DataAccessException.class, () -> ...)`. Es importante que el SP comunique el error adecuadamente y no cause corrupción.

## Automatización en CI
Los tests de SP no deberían ser excesivos; los más críticos se ejecutan junto a las pruebas de integración con una base de datos real (PostgreSQL, MySQL) levantada como contenedor en el pipeline.

## Rol del SDET
Colabora con los desarrolladores de back-end para identificar SP que carecen de cobertura de pruebas unitarias y escribe suites de integración que los verifiquen. También asegura que los SP formen parte de la estrategia de despliegue con rollback y puedan auditarse.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Consultas Avanzadas](./Consultas-avanzadas.md) | [Home](../../index.md) | [NoSQL Index](../NoSQL/index.md) |