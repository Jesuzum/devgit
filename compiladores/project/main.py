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
"""
Prueba para elementos anidados
use strict;
use warnings;

# Declaramos algunas variables para la prueba.
my $condicion = 1;
my $contador = 0;

# Estructura condicional principal.
if ($condicion) {
    print "Dentro del if principal.\n";
    
    # Mientras se cumpla la condición, se ejecuta el while.
    while ($contador < 3) {
        print "  Dentro del while: contador = $contador\n";
        
        # Para cada iteración del while, se ejecuta un ciclo for.
        for (my $i = 0; $i < 2; $i++) {
            print "    Dentro del for: i = $i\n";
        }
        
        $contador++;
    }
} else {
    print "Dentro del else.\n";
}

# Estructura if-else adicional para probar la anidación.
if (0) {
    print "Este bloque if no se ejecuta.\n";
} else {
    print "Bloque else correctamente ejecutado.\n";
}

"""
"""
anidacion con errores
use strict;
use warnings;

my $condicion = 1;
my $contador = 0;

if ($condicion) {
    print "Dentro del if principal.\n";
    
    while ($contador < 3) {
        print "Dentro del while: contador = $contador\n";
        
        # ERROR: El ciclo for inicia pero se omite la llave de cierre '}'.
        for (my $i = 0; $i < 2; $i++) {
            print "Dentro del for: i = $i\n";
        # Aquí falta la llave de cierre para el for.

        $contador++;
    }  # Supuestamente cierra el while, pero el for sigue abierto.
}  # Cierra el if.

else {
    print "Dentro del else.\n";
}
"""