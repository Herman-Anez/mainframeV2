# metacaracteres.md
Definición

Un metacaracter es un símbolo que en una expresión regular tiene un significado especial, no se interpreta de manera literal. Para tratarlo como un carácter normal hay que escaparlo anteponiendo una barra invertida \.
Lista de metacaracteres estándar

En la mayoría de los motores, los metacaracteres son:
text

. ^ $ * + ? { } [ ] \ | ( )

Cada uno tiene uno o varios roles según el contexto. Vamos a desgranarlos.
. (punto)

Coincide con cualquier carácter excepto un salto de línea (\n). En algunos motores, si se activa el flag s (DOTALL), también coincide con saltos de línea.
regex

a.b → "aab", "a3b", "a b", pero NO "a\nb" (sin flag s)

^ (circunflejo / sombrerito)

Doble función:

    Ancla de inicio: colocado al principio de la regex (o justo tras un |) indica comienzo de línea (o de cadena, según el flag m).

    Negación en clases: si es el primer carácter dentro de [^...], invierte la clase.

regex

^hola → "hola mundo" coincide (inicio)
[^0-9] → cualquier carácter no dígito

$ (dólar)

Ancla de fin: colocado al final (o justo antes de un | y cierre) indica final de línea o de cadena.
regex

mundo$ → "hola mundo" coincide al final

* + ? (cuantificadores simples)

    *: 0 o más repeticiones.

    +: 1 o más repeticiones.

    ?: 0 o 1 repetición, y también convierte cuantificadores en perezosos (*?, +?).

regex

a* → "", "a", "aaaa"
a+ → "a", "aaaa" (pero no "")
a? → "" o "a"

Pueden aplicarse a un carácter, clase o grupo.
{n,m} (cuantificador de intervalo)

Define un número exacto o rango de repeticiones.
regex

a{3} → exactamente "aaa"
a{2,4} → entre 2 y 4 "a"s
a{3,} → 3 o más
a{,5} → hasta 5 (raramente usado, según motor)

[ ] (clase de caracteres)

Define un conjunto de caracteres; coincide con un solo carácter que esté en la lista.
regex

[aeiou] → cualquier vocal
[0-9a-fA-F] → dígito hexadecimal
[^...] → negación (cualquiera que no esté)

Dentro de los corchetes muchos metacaracteres pierden su significado especial (solo algunos lo mantienen, ver más en clases_de_caracteres.md).
\ (barra invertida)

Símbolo de escape. Se usa para:

    Convertir un metacaracter en literal: \. busca un punto literal.

    Iniciar clases predefinidas: \d, \w, etc.

    Denotar anclas: \b, \B.

    Indicar secuencias especiales: \n (nueva línea), \t (tabulador).

| (tubería / alternancia)

Operador OR. Hace que la regex coincida con la expresión de la izquierda o con la de la derecha. Tiene la precedencia más baja, por lo que conviene delimitar con paréntesis.
regex

gato|perro → "gato" o "perro"
a(b|c)d → "abd" o "acd"

( ) (paréntesis)

Cumplen dos propósitos:

    Agrupar partes de la expresión para aplicar cuantificadores o alternancia.

    Capturar la subcoincidencia para usarla después (retroreferencias, extracción).
    Existen variantes:

    (?:...) grupo sin captura.

    (?<nombre>...) grupo con nombre.

    (?=...) aserciones (lookahead).

Metacaracteres que cambian de rol dentro de clases [ ]

Dentro de los corchetes, sólo son metacaracteres: \, ^ (sólo al inicio), - (en medio) y ] (que debe ser el primero o escaparse). Los demás . * + ? { } ( ) | se tratan como literales.
text

[.+*?] → coincide con uno de esos símbolos literalmente.
[a-z] → rango.
[-a] → guion literal si es el primero o inmediato después de ^.
[^a] → negación.

Siempre escapar [ y ] si aparecen fuera de su función.
