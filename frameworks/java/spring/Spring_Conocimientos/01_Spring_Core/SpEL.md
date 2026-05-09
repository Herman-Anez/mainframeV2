# SpEL: El lenguaje de expresiones de Spring

SpEL (Spring Expression Language) permite evaluar expresiones en tiempo real sobre un contexto de objetos. Integrado profundamente en el framework, es el motor oculto tras `@Value`, las condiciones de seguridad `@PreAuthorize`, las claves de caché `@Cacheable(key=...)`, los filtros de Spring Integration, etc.

## Sintaxis básica

Todo va entre `#{}`. Puedes incluir literales, operadores, acceso a propiedades, invocación de métodos, colecciones, operadores seguros, etc.

```java
@Value("#{ 2 + 3 }")
private int suma; // 5

@Value("#{ T(java.lang.Math).random() * 100.0 }")
private double numeroAleatorio;

@Value("#{ sistemaProperties['user.home'] }")
private String homeDir;

@Value("#{ miBeanDelContexto.propiedad }")
private String valorDeOtroBean;
```

## Operadores y tipos

- **Aritméticos:** `+`, `-`, `*`, `/`, `%`.
- **Comparación:** `==`, `!=`, `<`, `>`, `<=`, `>=`, `lt`, `gt`, `eq`, etc.
- **Lógicos:** `and`, `or`, `not`.
- **Condicional ternario:** `expression ? valorSiTrue : valorSiFalse`.
- **Elvis:** `nombre ?: 'Anónimo'` (si es `null`, usa el valor por defecto).
- **Safe navigation:** `objeto?.propiedad` (si objeto es `null`, devuelve `null` sin lanzar `NullPointerException`).
- **Expresiones regulares:** `'texto' matches '\\w+'`.
- **Tipo T:** `T(paquete.Clase)`. Accede a métodos estáticos y constantes.

## Acceso al contexto y beans

En una expresión puedes acceder a beans por su nombre con `@nombreBean` y al Environment mediante `environment['clave']` o `systemProperties`, `systemEnvironment` como objetos predefinidos.

```java
@Value("#{ @pedidoService.findById(#id) }") // Referencia a otro bean y su método
private Pedido obtenerPedido(Long id);
```

En `@PreAuthorize` de seguridad:

```java
@PreAuthorize("hasRole('ADMIN') or #usuario.id == authentication.principal.id")
public void actualizarPerfil(Usuario usuario) { ... }
```

## Uso en anotaciones de caché

```java
@Cacheable(value = "productos", key = "#nombre.toUpperCase()")
public Producto buscar(String nombre) { ... }
```

## Uso en Spring Integration y otras áreas

- **Filtros de mensajes:** `@Filter(inputChannel="...", expression="#payload.importe > 1000")`.
- **Transformadores:** `@Transformer(expression = "payload.nombre.toUpperCase()")`.

## StandardEvaluationContext y evaluación programática

Puedes evaluar SpEL manualmente para tus propias necesidades:

```java
ExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression("nombre.length() > 5");
StandardEvaluationContext context = new StandardEvaluationContext(objeto);
context.setVariable("descuento", 0.1);
Boolean result = exp.getValue(context, Boolean.class);
```

El contexto se puede nutrir con variables, funciones y root objects.

## Buenas prácticas y precauciones

- **Rendimiento:** las expresiones SpEL se compilan en árboles de sintaxis abstracta la primera vez, pero evaluarlas repetidamente en tiempo real tiene costo. Se recomienda compilar una vez y reutilizar el objeto `Expression`.
- **Legibilidad:** no abuses de SpEL en `@Value` para lógica muy compleja. Si una expresión se vuelve difícil de leer, extrae la lógica a un método Java.
- **Seguridad:** por defecto, SpEL no evalúa código arbitrario, pero en versiones muy antiguas era un vector de ataque. Siempre mantén las dependencias actualizadas.
- **Compatibilidad:** en `application.properties`, no se puede usar SpEL para definir propiedades (solo `@Value` al inyectarlas).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Perfiles](./Profiles.md) | [Índice](../../index.md) | [Conceptos de AOP](../02_AOP/Conceptos_JoinPoint_Pointcut_Advice.md) |
