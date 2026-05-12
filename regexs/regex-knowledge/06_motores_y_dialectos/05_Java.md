# Java.md
Motor java.util.regex

Java incluye un motor de regex rico en características, aunque no tan completo como PCRE o .NET. Se basa en backtracking y ofrece:

    Lookahead positivo/negativo.

    Lookbehind positivo/negativo con longitud máxima finita (debe poder determinarse un máximo de caracteres consumidos).

    Grupos atómicos (?>...).

    Cuantificadores posesivos *+, ++, ?+, {n,m}+.

    Grupos con nombre (?<name>...) (desde Java 7).

    Propiedades Unicode \p{...} (ej. \p{Lu}, \p{IsLatin}).

    Condicionales NO soportados (a diferencia de PCRE/.NET).

    Recursión, subrutinas, \K: no soportados.

    Flags: Pattern.CASE_INSENSITIVE, MULTILINE, DOTALL, UNICODE_CHARACTER_CLASS, COMMENTS (verboso), CANON_EQ, UNIX_LINES.

Lookbehind con límite finito

Java permite cuantificadores dentro del lookbehind siempre que tengan un límite superior explícito. * y + solos están prohibidos porque no hay máximo finito; en su lugar se deben usar {0,n}.
java

Pattern p = Pattern.compile("(?<=a{1,10})b"); // válido
Pattern.compile("(?<=a+)b"); // ERROR: Look-behind pattern does not have an obvious maximum length

Las alternativas pueden tener longitudes diferentes.
Clases Character y Unicode

Con la flag Pattern.UNICODE_CHARACTER_CLASS (o (?U)), las clases predefinidas \w, \d, \s siguen el estándar Unicode. Sin ella, \d es [0-9] y \w es [a-zA-Z0-9_].
java

Pattern p = Pattern.compile("\\w+", Pattern.UNICODE_CHARACTER_CLASS);
Matcher m = p.matcher("café");
// Con UNICODE_CHARACTER_CLASS, 'é' es parte de \w.

Grupos con nombre (Java 7+)
java

Pattern p = Pattern.compile("(?<year>\\d{4})-(?<month>\\d{2})");
Matcher m = p.matcher("2024-12");
String year = m.group("year");

La retroreferencia interna se hace con \k<name>.
Ejemplo de grupo atómico
java

String patron = "(?>a+)b";
Pattern.compile(patron).matcher("aaab").find(); // true
Pattern.compile(patron).matcher("aaaa").find(); // false (sin backtrack)

Flags y modo verboso

Java soporta el flag COMMENTS (equivalente a x de Perl). Permite espacios y comentarios en el patrón.
java

Pattern p = Pattern.compile(
    "^         # inicio\n" +
    "(\\d{4})  # año\n" +
    "$",
    Pattern.COMMENTS
);

Limitaciones principales respecto a PCRE/.NET

    No hay recursión ni subrutinas.

    No hay \K.

    No hay condicionales.

    El lookbehind debe tener un máximo finito; no se puede escribir (?<=.*)x.

    No hay verbos de control como (*SKIP).

Consejos

    Precompilar los patrones con Pattern.compile para reutilizarlos.

    Escapar bien las barras invertidas en las cadenas Java: \\d, \\s.

    Para texto internacional, usa Pattern.UNICODE_CHARACTER_CLASS.

    Si necesitas funcionalidades no presentes, evalúa usar una biblioteca externa o procesamiento adicional.

Ejemplo práctico

Validar un código postal español (5 dígitos) permitiendo un grupo opcional de 4 dígitos tras guión:
java

Pattern cp = Pattern.compile("^(\\d{5})(?:-(\\d{4}))?$");
Matcher m = cp.matcher("28001-1234");
if (m.find()) {
    String codigo = m.group(1); // "28001"
    String extensión = m.group(2); // "1234"
}
