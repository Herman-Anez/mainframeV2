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


