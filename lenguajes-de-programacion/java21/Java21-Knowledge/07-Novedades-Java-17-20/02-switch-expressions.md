# SWITCH EXPRESSIONS

Las Switch Expressions fueron introducidas como preview en Java 12 y se estandarizaron en Java 14. Permiten usar switch como una expresión que devuelve un valor, evitando la típica necesidad de variables temporales y break. Aportan un código más conciso y eliminan la fuente de bugs por olvido de break.
Forma con flecha ->
```java
int diaSemana = 3;
String nombreDia = switch (diaSemana) {
    case 1 -> "Lunes";
    case 2 -> "Martes";
    case 3 -> "Miércoles";
    default -> "Desconocido";
};
```

La flecha asocia directamente el caso con el valor devuelto o con una sentencia; no se requiere break y no hay fall‑through accidental (solo se ejecuta ese caso). Cada caso puede contener una única expresión o un bloque de código que debe finalizar con yield para devolver un valor.
Bloque con yield

Si un caso requiere varias instrucciones antes de devolver el valor, se usa un bloque y la palabra clave yield:
```java
String categoria = switch (diaSemana) {
    case 1, 7 -> {
        System.out.println("Fin de semana!");
        yield "Descanso";
    }
    case 6 -> {
        System.out.println("Viernes");
        yield "Casi finde";
    }
    default -> "Laborable";
};
```

yield tiene un ámbito léxico; no se puede usar fuera de un bloque de caso en una expresión switch.
Múltiples etiquetas por caso

Se pueden agrupar varios casos utilizando comas:
```java
case 1, 2, 3 -> "Inicio de mes";
```

### Exhaustividad

El compilador exige que una expresión switch cubra todos los posibles valores del tipo sobre el que se aplica. Es decir, debe ser exhaustiva. Para enum, hay que cubrir todos los literales o incluir default; para int, con default basta. Si no es exhaustiva, error de compilación.

Diferencias con el switch tradicional (sentencia):
Tradicional	Expresión (Java 14+)
Cada case necesita break	Usa -> o yield
No devuelve valor	Devuelve un valor
Permite fall‑through	No hay fall‑through con ->
No tiene requisito de exhaustividad	Requiere exhaustividad
default opcional	default opcional pero puede ser necesario según el tipo
Uso como sentencia con flecha

También se puede usar la notación -> en un switch que actúa como sentencia (no devuelve valor):
```java
switch (comando) {
    case "iniciar" -> System.out.println("Iniciando...");
    case "parar"   -> System.out.println("Parando...");
    default        -> System.out.println("Comando desconocido");
}
```

En este caso no se requiere exhaustividad, es una sentencia tradicional con sintaxis moderna.
Combinación con Pattern Matching (Java 21)

En Java 21, el switch se expande con pattern matching, convirtiéndose en una herramienta central para el polimorfismo. Las switch expressions con patrones permiten descomponer records y comprobar tipos de forma elegante, heredando toda la potencia de las expresiones descritas aquí.
