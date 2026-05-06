# Gestión de Transacciones con @Transactional

Spring abstrae el manejo de transacciones a través de la interfaz **`PlatformTransactionManager`**. Independientemente de si utilizas JDBC, JPA, Hibernate o incluso JMS, el modelo de programación declarativa sigue siendo el mismo.

---

## 1. El Modelo de Transacciones de Spring

La anotación `@Transactional` envuelve la ejecución de un método dentro de un proxy de Programación Orientada a Aspectos (AOP). Este proxy se encarga de abrir, unir, confirmar o revertir la transacción según sea necesario.

### Configuración Avanzada de @Transactional

```java
@Transactional(
    propagation = Propagation.REQUIRED,
    isolation = Isolation.READ_COMMITTED,
    timeout = 30,
    readOnly = false,
    rollbackFor = { RuntimeException.class },
    noRollbackFor = { MiExcepcionControlada.class }
)
public void procesarPedido() {
    // Lógica de negocio...
}
```

---

## 2. Propagación de Transacciones

Define cómo se comporta el método si ya existe una transacción en curso.

| Valor | Comportamiento |
| :--- | :--- |
| **`REQUIRED`** (defecto) | Se une a la transacción existente o crea una nueva si no hay ninguna. |
| **`REQUIRES_NEW`** | Siempre crea una transacción nueva, suspendiendo la actual si existe. |
| **`MANDATORY`** | Exige una transacción previa; si no existe, lanza una excepción. |
| **`SUPPORTS`** | Si existe una transacción, se une; si no, ejecuta de forma no transaccional. |
| **`NOT_SUPPORTED`** | Siempre ejecuta sin transacción, suspendiendo la actual. |
| **`NEVER`** | Lanza excepción si se invoca dentro de una transacción. |
| **`NESTED`** | Crea un punto de guardado (savepoint) anidado (solo compatible con JDBC). |

---

## 3. Aislamiento y Reversión (Rollback)

- **Isolation**: Define el nivel de visibilidad de los datos entre transacciones concurrentes (ej. `READ_COMMITTED`, `REPEATABLE_READ`).
- **Rollback For**: Por defecto, Spring solo realiza rollback ante excepciones de tipo **`RuntimeException`** o **`Error`**. Las excepciones comprobadas (*checked exceptions*) no provocan rollback a menos que se especifique explícitamente con `rollbackFor`.

---

## 4. El Proxy Transaccional y la Auto-Invocación

> [!CAUTION]
> **El problema de la auto-invocación**: Si un método dentro de una clase llama a otro método `@Transactional` de la misma clase usando `this.metodo()`, el proxy AOP es ignorado y la transacción **no se iniciará**.
> 
> **Solución**: Refactorizar el método a un bean diferente o inyectar el propio bean (auto-inyección).

---

## 5. Transacciones en Servicios vs Repositorios

- **Repositorios**: Spring Data JPA ya incluye transaccionalidad por defecto (ej. `readOnly = true` para consultas).
- **Servicios**: Es la ubicación recomendada para `@Transactional`, ya que un método de servicio suele orquestar múltiples llamadas a repositorios que deben ejecutarse como una única unidad atómica de trabajo.

---

## 6. Transacciones Distribuidas (JTA)

Cuando tu aplicación necesita coordinar cambios en múltiples recursos (ej. dos bases de datos diferentes o una base de datos y una cola de mensajes JMS), se requiere un gestor de **Java Transaction API (JTA)**. Spring Boot facilita la integración con implementaciones como **Atomikos**.

---

## 7. Testing de Transacciones

En pruebas de integración con `@SpringBootTest` o `@DataJpaTest`, marcar el método de prueba con `@Transactional` hará que cada test realice un rollback automático al finalizar, manteniendo la base de datos limpia.

> [!IMPORTANT]
> Si el test usa un cliente HTTP (como `TestRestTemplate`), la petición corre en un hilo separado del hilo del test y **no compartirá** la transacción, por lo que los cambios persistirán.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | :--- |
| [← Consultas Nativas](Consultas_Nativas_y_Procedure.md) | [Índice](../../README.md) | [Arquitectura de Seguridad →](../06_Seguridad/Spring_Security_Arquitectura.md) |

