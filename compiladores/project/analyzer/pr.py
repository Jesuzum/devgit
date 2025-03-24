# palabras validas para nombres de variables
palabras_reservadas = [
    "package", "use base", "sub", "my", "our", "isa", "new", "bless", 
    "SUPER", "ref", "use", "require", "do", "BEGIN", "END", "local", 
    "caller", "AUTOLOAD", "continue", "state", "unless", "for", "foreach", 
    "if", "elsif", "else", "while", "until", "last", "next", "redo", "and", 
    "or", "xor", "not", "exit", "die", "import", "defined", "undef", "exists", 
    "DESTROY", "return", "strict", "warnings", "constant", "open", "close",
]

# Funciones incorporadas
funciones_incorporadas = [
    "abs", "int", "rand", "sqrt", "length", "index", "lc", "uc", "lcfirst", 
    "ucfirst", "chr", "ord", "reverse", "substr", "split", "join", "push", 
    "pop", "shift", "unshift", "splice", "sort", "map", "grep", "defined", 
    "undef", "exists", "die", "exit", "eval", "require", "import", "caller", 
    "glob", "print", "say", "warn", "open", "close", "read", "write", "sysread", 
    "syswrite", "seek", "fileno", "flush", "binmode", "getline", "tell", 
    "eof", "chomp", "chop", "each", "keys", "values", "tie", "untie", "bless", 
    "ref", "isa", "new", "SUPER", "AUTOLOAD"
]

def es_palabra_reservada(token):
    return token in palabras_reservadas

def es_funcion_incorporada(token):
    return token in funciones_incorporadas
