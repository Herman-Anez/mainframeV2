
#  ¿Qué es un SDET? (Profundización)

El término SDET va más allá de “un tester que programa”. Representa un cambio de paradigma en la calidad de software: en lugar de verificar el producto al final, el SDET construye sistemas que integran calidad en cada paso.
Origen y evolución

Nació en Microsoft en 2005 bajo el título Software Development Engineer in Test, aunque el rol ya existía de facto en equipos de alta ingeniería. Posteriormente Google lo adoptó como Software Engineer in Test (SET), diferenciándolo del tester tradicional. La necesidad surgió al observar que los testers manuales se convertían en un cuello de botella en los ciclos de entrega continua. No se trataba de reemplazarlos, sino de añadir un perfil que pudiera:

    Entender el código del producto al mismo nivel que un desarrollador.

    Escribir herramientas de prueba reusables, no solo scripts lineales.

    Automatizar la infraestructura de pruebas: generación de datos, entornos efímeros, paralelización.

    Participar en revisiones de arquitectura para garantizar testabilidad desde el diseño.

Las tres dimensiones del rol

Un SDET opera en tres ejes simultáneos, lo que define su perfil único:

    Ingeniería de software: Aplica patrones de diseño, principios SOLID, control de versiones avanzado, refactorización y mentalidad de producto en el código de pruebas. No escribe scripts desechables; construye frameworks con APIs bien definidas.

    Conocimiento del dominio de pruebas: Sabe diseñar casos de prueba usando técnicas como partición equivalente, valores límite, tablas de decisión y testing exploratorio. Conoce las pirámides de testing, estrategias shift-left y cómo medir cobertura de código y de requisitos.

    Operaciones/DevOps: Entiende pipelines CI/CD, contenedores, orquestación, monitoreo de pruebas en producción (synthetic monitoring) y cómo integrar la ejecución de pruebas en el flujo de entrega.

Valor diferencial en las organizaciones

    Velocidad: Las pruebas se ejecutan en minutos, no en días. Los SDETs habilitan la integración continua real, donde cada commit dispara automáticamente miles de pruebas en paralelo.

    Estabilidad: Al tratar las pruebas como código de producción, reducen drásticamente los flaky tests (pruebas intermitentes) con buenas prácticas de esperas, aislamiento y reintentos inteligentes.

    Escalabilidad: Un único SDET puede construir un framework que usen 20 desarrolladores para escribir pruebas de forma autónoma, multiplicando la capacidad de testing.

    Cultura de calidad: Colabora con desarrollo para que la calidad sea responsabilidad de todos, no solo de un equipo de QA al final del ciclo.

#  Diferencias entre roles (Profundización)

Es crucial no solo listar los roles, sino entender las intersecciones y cómo varían sus actividades diarias, responsabilidades y habilidades.
Mapeo de responsabilidades típico
Actividad	QA Manual	QA Automation Engineer	SDET
Ejecutar casos de prueba manuales	Principal	Ocasional (regresiones no automatizables)	Rara vez (solo exploración técnica)
Automatizar scripts de pruebas existentes	No	Principal (mantener suite)	Sí, pero diseña el framework, no solo scripts
Diseñar frameworks desde cero	No	Básico (puede extender)	Principal
Programar componentes reusables (APIs, servicios)	No	Poco	Avanzado
Escribir pruebas unitarias/de integración del producto	No	No	Colabora, establece estándares
Participar en la arquitectura del sistema	No	No	Sí (revisiones de diseño)
Gestionar pipelines CI/CD (groovy, yaml)	No	Básico (disparar jobs)	Completo: creación, optimización, paralelización
Pruebas de rendimiento/seguridad	No	Ejecuta scripts dados	Diseña los planes, crea los scripts y analiza resultados
Revisar código del producto	No	No	Sí (peer review)
Mentorizar desarrolladores en testing	No	Poco	Frecuente (cultura de calidad)
La falsa jerarquía

Comúnmente se cree que QA Manual → QA Automation → SDET es una progresión natural, pero es engañoso. Un SDET puede provenir de desarrollo de software sin haber sido nunca tester manual. La diferencia fundamental está en la mentalidad de ingeniería: un QA Automation Engineer a menudo se limita a traducir casos manuales a código; un SDET piensa en cómo las pruebas deben modelar el sistema bajo prueba, con principios de diseño de software.
Caso práctico: migración de suite de pruebas

    QA Automation Engineer: Toma 200 casos de prueba en TestRail, implementa uno a uno en Selenium, usa Page Object Model copiado de un tutorial. Si la UI cambia drásticamente, actualiza manualmente los selectores en cada script.

    SDET: Analiza el sistema, identifica componentes reutilizables, diseña una capa de abstracción de UI con Screenplay o componentes web genéricos. Crea un DSL (lenguaje específico de dominio) para que los testers puedan escribir pruebas en lenguaje casi natural. Ante un cambio de UI, modifica solo la capa de localización y recompone los tests sin tocarlos. Además integra variables de entorno y ejecución paralela desde el inicio.

Habilidades comparativas

    QA Manual: Gran capacidad analítica, ojo para detalles, dominio de técnicas de prueba, empatía con el usuario.

    QA Automation Engineer: Programación a nivel de scripting (orientado a procedimientos), manejo de selectores y herramientas, ejecución de suites.

    SDET: Programación orientada a objetos/funcional avanzada, diseño de software, conocimiento de protocolos de red, bases de datos, sistemas operativos, CI/CD, a menudo nivel similar a un desarrollador backend.

#  Pirámide de Testing (Profundización)

La pirámide de testing de Mike Cohn (2009) es el modelo mental más importante para un SDET. No es una regla rígida, sino una guía de proporciones y velocidad.
Capas clásicas y propósito
text

        /\
       /  \          UI / End-to-End
      /    \         (Pocas, lentas, frágiles)
     /------\
    /        \       Integración / Servicio
   /          \      (Cantidad media, velocidad media)
  /------------\
 /              \    Unitarias
/________________\   (Muchas, rápidas, estables)

    Pruebas Unitarias (base)

        Qué prueban: La unidad más pequeña de código aislada (función, método, clase). Sin dependencias externas reales (se usan dobles como mocks/stubs).

        Quién las escribe: Principalmente desarrolladores, pero el SDET define el framework, las políticas de cobertura y las complementa.

        Características: Ejecución en milisegundos, no requieren entorno (todo en memoria). Deben ser miles.

        Ejemplo: Verificar que un método CalcularDescuento(precio, porcentaje) devuelve el valor correcto con distintos parámetros.

    Pruebas de Servicio/Integración (capa intermedia)

        Qué prueban: La comunicación entre módulos, APIs, acceso a base de datos, colas de mensajes, contratos entre servicios.

        Aquí es donde el SDET más brilla. Automatiza pruebas de API REST, GraphQL, gRPC, mensajería asíncrona (Kafka), pruebas de contrato (Pact) y de integración con bases de datos.

        Características: Más lentas que las unitarias (implican red, E/S). Se ejecutan contra servicios reales, a veces en contenedores Docker. Debe haber muchas, pero en menor cantidad que las unitarias.

        Ejemplo: Enviar una petición POST a /usuarios y validar que el código de estado es 201, el cuerpo contiene un ID y que el registro se insertó realmente en la base de datos. O verificar que al publicar un mensaje en un topic, el consumidor lo procesa correctamente.

    Pruebas de UI / End-to-End (punta)

        Qué prueban: Flujos completos a través de la interfaz de usuario (web, móvil) simulando un usuario real.

        Características: Extremadamente lentas (segundos por acción), frágiles (dependen de tiempos de renderizado, red, selectores). Deben ser muy pocas, solo los flujos críticos de negocio (happy paths, compra, login, registro).

        Ejemplo: Abrir navegador, ir a la tienda, buscar un producto, añadirlo al carrito, hacer checkout y verificar el resumen de pedido.

Variantes modernas

    Testing Trophy (Kent C. Dodds): Enfatiza las pruebas de integración estáticas (con React Testing Library) por sobre las unitarias puras. Para un SDET en frontend, el trofeo invierte un poco la pirámide: énfasis en pruebas de componentes integrados.

    Honeycomb (Spotify): Para sistemas con muchos microservicios y pocas UI, se enfoca en pruebas de integración entre servicios, endpoints y contratos.

    Principio común: Aumentar la confianza reduciendo el costo y el tiempo de feedback. Un SDET siempre está empujando el testing hacia las capas más bajas.

Cómo aplica el SDET la pirámide

    Audita la cobertura actual: ¿hay demasiadas pruebas UI y pocas de API? Propone migrar esos escenarios a la capa de servicio.

    Diseña el framework para que escribir pruebas de integración sea tan fácil como escribir unitarias (patrones reusables, clientes API preconfigurados).

    Implementa la suite de regresión UI solo con smoke tests (pruebas de humo) que validen que todo el sistema en conjunto funciona, y mueve las regresiones detalladas a servicios.

#  Ciclo de vida del software y el SDET

El SDET no se suma al final; su actividad cubre todo el ciclo de vida, particularmente en metodologías ágiles (Scrum, Kanban) y DevOps.
Fases típicas y participación

    Planificación / Refinamiento de backlog

        Revisa historias de usuario junto a Product Owner y desarrolladores.

        Aporta criterios de aceptación desde la perspectiva de prueba: condiciones de borde, escenarios negativos, requisitos de rendimiento.

        Identifica dependencias técnicas que pueden dificultar la automatización (p.ej., falta de IDs en los elementos UI) y las eleva como tareas técnicas.

        Estima el esfuerzo de automatización.

    Diseño

        Participa en las sesiones de diseño de arquitectura para sugerir puntos de prueba: exponer endpoints de health-check, habilitar logs estructurados, prever inyección de dependencias para testing, diseñar APIs con idempotencia y fácil testabilidad.

        Diseña la estrategia de pruebas para las nuevas funcionalidades: ¿qué se probará unitario, integración, UI? ¿Se necesitan pruebas de contrato?

        Define los datos de prueba necesarios y cómo se generarán.

    Desarrollo (Codificación)

        Mientras los desarrolladores programan, el SDET:

            Escribe las pruebas de API/integración en paralelo, a veces antes del código (ATDD – Acceptance Test-Driven Development).

            Configura el entorno de pruebas (docker-compose con servicios mockeados o reales).

            Prepara los scripts de carga de datos.

            Revisa el código del producto (pull request) enfocándose en la testabilidad y en las pruebas unitarias que el desarrollador incluyó.

        Integra las pruebas en el pipeline CI para que se ejecuten en cada push.

    Pruebas (Fase de verificación explícita)

        En lugar de ejecutar pruebas manuales, el SDET ejecuta y monitorea las suites automáticas.

        Analiza los resultados fallidos: si son bugs, reporta con precisión (logs, trazas, pasos para reproducir); si son falsos positivos, ajusta el script.

        Realiza pruebas exploratorias dirigidas a áreas de alto riesgo que no están automatizadas (porque no todo es automatizable).

        Ejecuta pruebas de rendimiento o de seguridad si la historia lo requiere.

    Liberación (Release) y despliegue

        Las pruebas de humo automáticas se ejecutan en el entorno de pre-producción como último filtro.

        Supervisa las métricas de negocio y errores en producción (synthetic monitoring, canary releases). Si hay un incidente, añade una prueba que lo capture para regresión futura.

    Mantenimiento y evolución

        Continuamente refactoriza el código de pruebas para mantenerlo limpio.

        Actualiza las herramientas de testing cuando hay nuevas versiones.

        Monitoriza la duración de la suite y optimiza la paralelización para mantener el feedback rápido.

Integración en DevOps: Shift-Left y Shift-Right

    Shift-Left: Mover las pruebas lo antes posible en el ciclo. Ejemplo: pruebas estáticas (linting, análisis de seguridad SAST) en el pre-commit; unitarias al hacer commit; integración en el build. El SDET ayuda a que los desarrolladores puedan ejecutar pruebas complejas localmente con un solo comando.

    Shift-Right: Probar en producción de forma controlada. El SDET implementa verificaciones sintéticas que golpean la aplicación desplegada periódicamente y disparan alertas si fallan. También participa en pruebas de caos (Chaos Engineering) y feature flags.

#  Técnicas de diseño de pruebas

Un SDET no solo escribe código, sino que sabe qué probar y cómo seleccionar los casos mínimos que maximizan la cobertura de fallos. Las técnicas abarcan caja negra, caja blanca y basadas en experiencia.
Técnicas de caja negra (sin ver código)

    Partición de equivalencia (Equivalence Partitioning)

        Divide los datos de entrada en grupos que se espera se comporten de manera similar. Se prueba un representante de cada partición.

        Ejemplo: Campo "edad" (válidos 0-120). Particiones: números negativos (inválido), 0-120 (válido), >120 (inválido), texto (inválido). No hace falta probar 5, 38 y 119; basta con un valor representativo de cada clase.

    Análisis de valores límite (Boundary Value Analysis)

        Complementa la anterior. Los errores suelen ocurrir en los bordes de las particiones.

        Ejemplo: Para rango 0-120, probar: -1, 0, 1, 119, 120, 121. En la práctica, mínimo, mínimo-1, máximo, máximo+1.

    Tablas de decisión

        Útiles para lógica compleja con combinaciones de condiciones y acciones.

        Ejemplo: Descuento según tipo de cliente (VIP/Regular) y monto de compra (>100, ≤100). Se construye una tabla con las 4 combinaciones posibles y se define el descuento esperado en cada caso.

    Transición de estados

        Para sistemas que cambian de estado según eventos (máquinas de estado). Se modelan estados y transiciones, y se diseñan casos para cubrir caminos: transiciones válidas, inválidas, ciclos.

        Ejemplo: Un pedido: Creado → Pagado → Enviado → Entregado. Probar el flujo feliz, intentar pagar un pedido ya enviado (transición inválida), etc.

    Pruebas de pares (Pairwise testing)

        Cuando hay muchos parámetros, probar todas las combinaciones es inviable. Se usa un algoritmo (como All-Pairs) para garantizar que cada par de valores de parámetros se prueba al menos una vez.

        Herramientas: PICT (Microsoft), ACTS. Un SDET puede integrar la generación de datos de prueba mediante estas herramientas.

Técnicas de caja blanca (estructurales, viendo el código)

    Cobertura de sentencias, ramas y caminos

        Asegurar que la suite unitaria ejecuta todas las líneas (sentencias), todas las decisiones verdadero/falso (ramas), y combinaciones de caminos base. El SDET revisa estas métricas con herramientas como JaCoCo/ Istanbul y decide si hay lagunas.

    Pruebas de mutación

        Van un paso más allá: introducen pequeños cambios (mutantes) en el código fuente y verifican si las pruebas los detectan. Si un mutante sobrevive, la suite de pruebas no es suficientemente robusta. Herramientas: PIT (Java), Stryker (JS/.NET). Un SDET avanzado configura pruebas de mutación en el pipeline para elevar la efectividad de las pruebas.

Técnicas basadas en la experiencia

    Testing exploratorio

        Aprendizaje simultáneo, diseño y ejecución de pruebas. No sigue un guion rígido. El SDET lo usa para identificar riesgos no contemplados por la automatización y luego valora si automatizarlos o mantenerlos como sesión exploratoria programada.

        Se gestiona con Session-Based Test Management (SBTM) usando charters (misiones).

    Pruebas basadas en riesgos

        Priorizar qué probar según el impacto y probabilidad de fallo. Matriz de riesgos: alto impacto + alta probabilidad → pruebas exhaustivas. Bajo impacto + baja probabilidad → pruebas mínimas o ninguna. El SDET aplica esto para decidir qué automatizar primero.

Diseño de casos con Gherkin (BDD)

    El SDET suele ser el facilitador de BDD. Escribe escenarios en Gherkin (Given/When/Then) que son legibles para el negocio y automáticamente ejecutables (con Cucumber, SpecFlow, Behave).

    Ejemplo:
    gherkin

    Scenario: Retirar dinero con saldo suficiente
      Given el cliente tiene una cuenta con saldo 500€
      When retira 200€
      Then el saldo de la cuenta debe ser 300€
      And el cajero debe dispensar 200€

    La calidad está en mantener estos escenarios atómicos, sin detalles de implementación y reutilizando pasos.

Aplicación práctica para el SDET

    Al recibir una historia de usuario, el SDET combina varias técnicas: define particiones de equivalencia para los datos de entrada, verifica los valores límite, modela la transición de estados si aplica y escribe escenarios BDD para los flujos principales.

    Luego, al implementar la automatización, codifica esas técnicas: el script puede iterar sobre un array de valores límite generados dinámicamente, no hardcodeados.


