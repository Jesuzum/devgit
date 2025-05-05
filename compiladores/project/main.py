from ui import ui_init

if __name__ == "__main__":
    ui_init()
"""
Sin errores

use strict;
use warnings;

# For clásico: se usa con una cabecera entre paréntesis
for (my $i = 0; $i < 5; $i++) {
    print "For clásico: iteración $i\n";
}

print "\n";

# For iterativo: se asume que se declara la variable y se proporciona una lista entre paréntesis
for $color ('rojo', 'verde', 'azul') {
    print "For iterativo: color $color\n";
}

"""
"""
Con errores
use strict;
use warnings;

# For clásico con error:
# El incremento debería ser "$i++", pero aquí se ha escrito "$i+++"
for (my $i = 0; $i < 5; $i+++) {
    print "Error: triple plus en el incremento\n";
}

# For iterativo con error:
# Falta el paréntesis de apertura después de la variable iteradora "$color".
for $color 'rojo', 'verde', 'azul') {
    print "Error: falta '(' en la sentencia for iterativo\n";
}
"""
"""
While sin errores
use strict;
use warnings;

# Declaramos una variable de control.
my $contador = 0;

# Sentencia while: se usa para iterar mientras $contador sea menor que 5.
while ($contador < 5) {
    print "Iteración while: contador = $contador\n";
    $contador++;
}
"""
"""
while con errores
use strict;
use warnings;

my $contador = 0;

# Error en el while:
# Se omite el paréntesis de apertura en la condición
while $contador < 5) {
    print "Error en while: contador = $contador\n";
    $contador++;
}
"""