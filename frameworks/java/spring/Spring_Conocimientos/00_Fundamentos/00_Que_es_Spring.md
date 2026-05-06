#  ¿Qué es Spring? La filosofía y el ecosistema

Spring no es simplemente un conjunto de utilidades. Es un marco de trabajo completo que redefine cómo se construye software empresarial en Java. Para entenderlo a fondo hay que responder a tres preguntas: ¿por qué surgió?, ¿qué problema resuelve realmente? y ¿cómo está diseñado?
El problema original: J2EE pesado

A principios de los 2000, desarrollar aplicaciones empresariales con J2EE (antecesor de Jakarta EE) implicaba un infierno de configuración XML, obligatoriedad de heredar de clases del servidor de aplicaciones (EjBs), interfaces remotas, despliegues larguísimos y código fuertemente acoplado. Spring nació en 2003 de la mano de Rod Johnson como una reacción contra esa complejidad, basándose en las ideas de su libro *Expert One-on-One J2EE Design and Development*.
Principios fundamentales de Spring

    Contenedor ligero: no necesitas un servidor de aplicaciones pesado; Spring puede ejecutarse en un simple Tomcat o incluso en un entorno standalone. Gestiona el ciclo de vida de los objetos (beans) sin imponer contratos como EJBObject o interfaces específicas.

    No invasivo: las clases de tu dominio o servicio no tienen que extender clases de Spring ni implementar interfaces del framework (salvo alguna interfaz opcional para conveniencia). Solo se usan anotaciones que son puras marcas o importaciones de javax.inject / Jakarta.

    Configuración por convención y anotaciones: en lugar de una montaña de XML, hoy se utiliza principalmente configuración por código Java y anotaciones, complementada con la autoconfiguración de Spring Boot.

    Modularidad: Spring se compone de una veintena de módulos que puedes usar o ignorar. El núcleo (spring-core, spring-beans, spring-context) es obligatorio; el resto se añade según necesidad.

Arquitectura general de Spring

Se organiza en capas:

    Core Container (spring-core, spring-beans, spring-context, spring-expression): el contenedor IoC, el lenguaje SpEL, manejo de beans, etc.

    AOP and Instrumentation (spring-aop, spring-aspects): programación orientada a aspectos.

    Data Access/Integration (spring-jdbc, spring-tx, spring-orm, spring-jms): abstracción sobre JDBC, JPA, transacciones y mensajería.

    Web (spring-web, spring-webmvc, spring-websocket, spring-webflux): soporte para MVC, WebSocket y reactivo.

    Test (spring-test): utilidades para pruebas unitarias y de integración.

Sobre estos bloques se construye el ecosistema Spring Boot (que empaqueta y autoconfigura todo), Spring Data, Spring Security, Spring Cloud, etc.
¿Qué no es Spring?

    No es un servidor de aplicaciones, aunque puede reemplazar gran parte de su funcionalidad.

    No es solo un framework de inyección de dependencias; DI es solo el pegamento.

    No obliga a usar solo su forma de hacer las cosas; puedes combinar XML y anotaciones, usar solo partes del ecosistema.

En resumen: Spring es una plataforma de productividad para Java empresarial que proporciona infraestructura, abstracciones y una filosofía de diseño limpia.
