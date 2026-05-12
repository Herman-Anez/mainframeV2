pcre_cheatsheet.pdf (contenido)
Metacaracteres básicos
Símbolo	Significado
.	Cualquier carácter excepto nueva línea (con s incluye \n)
^	Inicio de cadena/línea (con m)
$	Fin de cadena/línea (con m)
*	0 o más
+	1 o más
?	0 o 1 / perezoso
{n}	Exactamente n
{n,}	n o más
{n,m}	Entre n y m
*+, ++, etc.	Posesivos
( ... )	Grupo de captura
(?: ... )	Grupo sin captura
(?<name>...)	Grupo con nombre
(?> ... )	Grupo atómico
|	Alternancia
\	Escape
Clases de caracteres
Símbolo	Equivalente
\d	Dígito [0-9] (con u Unicode)
\D	No dígito
\w	Carácter de palabra [a-zA-Z0-9_] (Unicode con u)
\W	No palabra
\s	Espacio blanco
\S	No espacio
\h	Espacio horizontal
\v	Espacio vertical
\R	Salto de línea universal
Anclas y límites
Símbolo	Significado
\b	Límite de palabra
\B	No límite
\A	Inicio absoluto
\z	Final absoluto
\Z	Final o antes de \n al final
Lookahead / Lookbehind
Constructo	Significado
(?=...)	Lookahead positivo
(?!...)	Lookahead negativo
(?<=...)	Lookbehind positivo (fijo o variable en PCRE2)
(?<!...)	Lookbehind negativo
Flags comunes
Flag	Descripción
i	Ignora mayúsculas
m	Multilínea
s	Dotall (. incluye \n)
x	Modo verboso
u	Unicode
U	Ungreedy (invertir codicia)
Avanzado PCRE
Constructo	Descripción
(?R), (?0)	Recursión (patrón completo)
(?1), (?2)	Recursión a grupo específico
(?&name)	Subrutina a grupo con nombre
\k<name>	Retroreferencia a grupo con nombre
\g{n}	Retroreferencia con número grande
(?(cond)si|no)	Condicional
\K	Descartar lo coincidido a la izquierda
(*SKIP)(*FAIL)	Saltar y fallar (control de backtrack)
(*COMMIT)	Confirmar avance sin retroceso
\p{L}, \p{Script=Latin}	Propiedades Unicode
Secuencias de escape
Secuencia	Significado
\n	Nueva línea
\r	Retorno de carro
\t	Tabulador
\x{2020}	Carácter Unicode (hex)
\Q...\E	Literal entre medias