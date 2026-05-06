# Acceso_Datos/Transacciones_y_Transactional.md
Modelo de transacciones de Spring

Spring abstrae las transacciones con PlatformTransactionManager. Independientemente de que uses JDBC, JPA o JMS, el manejo declarativo es el mismo. La anotación @Transactional envuelve el método en un proxy AOP que crea/únete a una transacción según la configuración.
@Transactional en profundidad
java

@Transactional(
    propagation = Propagation.REQUIRED,
    isolation = Isolation.READ_COMMITTED,
    timeout = 30,
    readOnly = false,
    rollbackFor = { RuntimeException.class },
    noRollbackFor = { MiExcepcionControlada.class }
)
public void procesarPedido() { ... }

Propagación: define cómo se comporta el método si ya existe una transacción.
Valor	Comportamiento
REQUIRED (defecto)	Usa la transacción existente o crea una nueva.
REQUIRES_NEW	Siempre crea una nueva transacción, suspendiendo la actual.
MANDATORY	Debe existir una transacción; si no, lanza excepción.
SUPPORTS	Ejecuta en transacción si existe, si no, no.
NOT_SUPPORTED	Siempre ejecuta sin transacción, suspendiendo la existente.
NEVER	No debe existir transacción; si hay, lanza excepción.
NESTED	Ejecuta en un savepoint anidado (solo con JDBC).

Isolation: nivel de aislamiento SQL (READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE). Normalmente READ_COMMITTED es suficiente.

readOnly: optimiza el rendimiento indicando que solo hay lecturas (el EntityManager no necesita hacer dirty checking).

rollbackFor / noRollbackFor: por defecto, solo se hace rollback con RuntimeException y Error. Si una excepción checked debe causar rollback, se especifica.
El proxy transaccional: cómo funciona internamente

    Spring crea un proxy alrededor del bean.

    Cuando se invoca un método anotado con @Transactional desde fuera del bean, el proxy intercepta la llamada.

    Antes de ejecutar el método, consulta al TransactionManager para comenzar o unirse a una transacción.

    Ejecuta el método real.

    Si el método lanza una excepción que cumple con rollbackFor, el TransactionManager hace rollback.

    Si todo sale bien, hace commit.

    Si la excepción es de las que no causan rollback, hace commit después de la excepción (poco común).

El problema de la auto-invocación: si desde dentro del mismo bean se llama a this.metodoTransaccional(), no pasa por el proxy y la anotación se ignora. Soluciones: autowirearse uno mismo, usar AopContext.currentProxy(), o refactorizar a otro bean.
@Transactional en repositorios y servicios

La práctica recomendada es poner @Transactional a nivel de servicio o caso de uso. Los repositorios de Spring Data JPA ya heredan @Transactional(readOnly = true) en SimpleJpaRepository para métodos de consulta, y los métodos de modificación (save, delete) tienen @Transactional por defecto, pero usualmente se requiere una transacción que cubra todo el flujo de negocio.
Transacciones y bases de datos distribuidas / JTA

Con un solo DataSource, se usa DataSourceTransactionManager o JpaTransactionManager. Para múltiples recursos (dos bases de datos, JMS, etc.) se necesita un gestor de transacciones distribuidas (JTA), como Atomikos o Bitronix, o delegar en el servidor de aplicaciones. Spring Boot simplifica la configuración con spring-boot-starter-jta-atomikos.
Manejo de transacciones largas y con patrones conversacionales

Spring soporta transacciones largas usando @Transactional y sesiones extendidas, pero la tendencia es usar arquitecturas que eviten mantener la transacción abierta a través de múltiples peticiones HTTP. En su lugar, se usa @Transactional en cada petición y se trabaja con entidades detachadas, volviendo a fusionarlas (merge) si es necesario.
Testing de transacciones

En pruebas con @DataJpaTest o @SpringBootTest, se puede usar @Transactional para que las operaciones de un test se reviertan automáticamente al final. Sin embargo, cuando se usa TestRestTemplate en @SpringBootTest(webEnvironment = RANDOM_PORT), la petición HTTP corre en un hilo separado, por lo que no comparte la transacción del test. En ese caso, se debe limpiar manualmente o usar @Transactional(propagation = NOT_SUPPORTED) y luego borrar datos.
