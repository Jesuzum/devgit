from lexer import AnalizadorLexico
from parser import AnalizadorSintactico
from semantic import AnalizadorSemantico 

codigo_prueba = """
use strict;
use warnings;

my $nombre = "Carlos";
my $salario = 50000;
my $bono = 5000;

sub calcular_salario_final {
    my ($base, $extra) = @_;
    return $base + $extra;
}

my $salario_final = calcular_salario_final($salario, $bono);

if ($salario_final > 60000) {
    print "Salario alto\\n";
} elsif ($salario_final > 55000) {
    print "Salario medio\\n";
} elsif ($salario_final < 50000) {
    print "Salario bajo\\n";
} else {
    print "Salario bajo\\n";
}

print "Empleado: $nombre\\n";
print "Salario final: $salario_final\\n";
"""

# Primero, generar tokens con el lexer.
analizador_lex = AnalizadorLexico()
analizador_lex.analizar(codigo_prueba)
tokens = analizador_lex.tokens

# Luego, análisis sintáctico.
analizador_sintactico = AnalizadorSintactico(tokens)
analizador_sintactico.parse()

# Finalmente, análisis semántico.
analizador_semantico = AnalizadorSemantico()
analizador_semantico.analizar(tokens)
analizador_semantico.mostrar_errores()