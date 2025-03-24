# main.py
from lexer import AnalizadorLexico
from parser import AnalizadorSintactico
from semantic import AnalizadorSemantico

def main():
    codigo_prueba = """
use strict;
use warnings;

my $nombre = "Carlos";
my $salario = 50000;
my $bono = 5000;

sub calcular_salario_final {
    my ($base, $bonus) = @_;  # Parámetros correctamente declarados.
    return $base + $bonus;
}

my $salario_final = calcular_salario_final($salario, $bono);

print "Empleado: $nombre\n";
print "Salario final: $salario_final\n";

    """
    codigo_error = """
use strict;
use warnings;

# Declaración global de variables
my $nombre = "Carlos";
my $nombre = "Pedro";  # ERROR: redeclaración de $nombre en el mismo ámbito.
my $salario = 50000;

# Función definida correctamente: recibe dos parámetros.
sub calcular_salario_final {
    my ($base, $bonus) = @_;  # Parámetros correctamente declarados.
    return $base + $bonus;
}

# Llamada a función con parámetro insuficiente (se esperaba 2, se proporciona 1).
my $salario_final = calcular_salario_final($salario);

# Llamada a función no declarada.
my $impuesto = calcular_impuestos($salario_final);

print "Empleado: $nombre\n";
print "Salario final: $salario_final\n";
print "Impuesto: $impuesto\n";

    """

    # Ejecutamos el análisis léxico.
    analizador_lex = AnalizadorLexico()
    analizador_lex.analizar(codigo_error)
    print("\n=== TOKENS GENERADOS POR EL LEXER ===")
    analizador_lex.mostrar_tokens()

    # Ejecutamos el análisis sintáctico.
    print("\n=== ANÁLISIS SINTÁCTICO ===")
    analizador_sint = AnalizadorSintactico(analizador_lex.tokens)
    analizador_sint.parse()
    analizador_sint.show_errors()

    # Ejecutamos el análisis semántico con los mismos tokens
    print("\n=== ANÁLISIS SEMÁNTICO ===")
    analizador_sem = AnalizadorSemantico()
    analizador_sem.analizar(analizador_lex.tokens)
    analizador_sem.mostrar_errores()

if __name__ == "__main__":
    main()
