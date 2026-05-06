# Integración de JPA y Hibernate

JPA (**Jakarta Persistence API**) es la especificación estándar para el Mapeo Objeto-Relacional (ORM) en Java. **Hibernate** es la implementación más popular y completa de este estándar. Spring Boot selecciona y configura Hibernate automáticamente si detecta el starter `spring-boot-starter-data-jpa` en el proyecto.

---

## 1. Configuración de JPA en Spring

En una aplicación Spring sin las facilidades de autoconfiguración de Boot, la configuración manual requiere definir el `EntityManagerFactory` y el gestor de transacciones:

```java
@Bean
public LocalContainerEntityManagerFactoryBean entityManagerFactory(DataSource ds) {
    LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
    emf.setDataSource(ds);
    emf.setPackagesToScan("com.empresa.modelo");
    emf.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
    emf.setJpaProperties(hibernateProperties());
    return emf;
}

@Bean
public PlatformTransactionManager transactionManager(EntityManagerFactory emf) {
    return new JpaTransactionManager(emf);
}
```

> [!NOTE]
> Spring Boot simplifica esto drásticamente permitiendo configurar todo mediante propiedades `spring.jpa.*` en el archivo `application.properties`.

---

## 2. El EntityManager y su Ciclo de Vida

El **`EntityManager`** es el objeto central de JPA que gestiona el ciclo de vida de las entidades. Spring, a través de la anotación `@PersistenceContext`, inyecta un proxy del `EntityManager` que está vinculado al ámbito de la transacción actual.

```java
@Repository
public class ProductoDao {
    @PersistenceContext
    private EntityManager em;

    public Producto findById(Long id) {
        return em.find(Producto.class, id);
    }
}
```

> [!IMPORTANT]
> El `EntityManager` real no es thread-safe. Por eso, Spring inyecta un proxy inteligente que delega en la instancia correcta según la transacción activa en el hilo de ejecución.

---

## 3. Entidades: Anotaciones Esenciales

Las clases Java se convierten en entidades de base de datos mediante anotaciones:

```java
@Entity
@Table(name = "productos")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String nombre;

    @Enumerated(EnumType.STRING)
    private Categoria categoria;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fabricante_id")
    private Fabricante fabricante;
    
    // Getters y Setters
}
```

### Estrategias de Generación de ID
- **`IDENTITY`**: Delega el incremento a la base de datos (común en MySQL).
- **`SEQUENCE`**: Usa una secuencia de base de datos (común en PostgreSQL y Oracle).
- **`AUTO`**: Deja que Hibernate elija la estrategia según el dialecto.

---

## 4. Mapeo de Relaciones

JPA soporta las relaciones estándar de bases de datos:
- **`@OneToOne`**, **`@OneToMany`**, **`@ManyToOne`**, **`@ManyToMany`**.

### Conceptos Críticos
- **Fetch Type**: Por defecto, `@ManyToOne` es `EAGER` (carga inmediata). Se recomienda encarecidamente cambiarlo a `LAZY` para evitar cargar grafos de objetos innecesarios.
- **MappedBy**: Se utiliza en el lado "no propietario" de una relación bidireccional para indicar qué atributo en la otra entidad define la relación, evitando la creación de tablas intermedias innecesarias.
- **`LazyInitializationException`**: Ocurre al acceder a una relación `LAZY` fuera de una transacción. Se soluciona manteniendo la transacción abierta (con `@Transactional`) o usando consultas con `JOIN FETCH`.

---

## 5. Hibernate como Motor: Propiedades Clave

Puedes personalizar el comportamiento de Hibernate en `application.properties`:

```properties
spring.jpa.show-sql=true
spring.jpa.hibernate.ddl-auto=validate  # validate, update, create, create-drop
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

> [!WARNING]
> En entornos de producción, `ddl-auto` debe ser siempre `validate` o `none`. Usar `update` puede causar cambios estructurales destructivos accidentales. Es mejor usar herramientas de migración como **Flyway** o **Liquibase**.

---

## 6. Contexto de Persistencia y Dirty Checking

Dentro de una transacción, el `EntityManager` mantiene una **Caché de Primer Nivel**. Esto garantiza que si pides la misma entidad varias veces, recibirás la misma instancia en memoria.

### Dirty Checking
Hibernate monitoriza los cambios en las entidades gestionadas. Al finalizar la transacción (o al hacer `flush`), compara el estado actual con la instantánea original y sincroniza los cambios automáticamente. **No es necesario llamar a un método "update"** si la entidad está en estado *managed*.

---

## 7. Operaciones con EntityManager

- **`persist(entity)`**: Inserta una nueva entidad.
- **`merge(entity)`**: Sincroniza el estado de una entidad *detached* con el contexto actual.
- **`remove(entity)`**: Elimina una entidad del contexto y de la base de datos.
- **`find(Class, id)`**: Busca por clave primaria.
- **`createQuery(jpql)`**: Ejecuta consultas orientadas a objetos.
- **`flush()`**: Sincroniza los cambios pendientes con la base de datos antes del commit.

---

## 8. Errores Frecuentes y Soluciones

1. **Problema N+1**: Al recorrer una lista de entidades y acceder a una relación lazy, se ejecuta una consulta extra por cada elemento.
   - **Solución**: Usar `JOIN FETCH` en JPQL o `@EntityGraph`.
2. **Entidades Detachadas**: Intentar operar sobre una entidad que ya no está vinculada al `EntityManager`.
   - **Solución**: Usar `merge()` para volver a vincularla.
3. **Falta de Transaccionalidad**: Olvidar `@Transactional` en la capa de servicios, lo que impide que Hibernate sincronice los cambios o gestione correctamente las sesiones.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | :--- |
| [← JDBC Template](JDBC_Template.md) | [Índice](../../README.md) | [Spring Data JPA →](Spring_Data_JPA.md) |

