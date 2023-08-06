def rojo(text):
    """Imprime el texto en color rojo"""
    return "\033[91m{}\033[0m".format(text)

def verde(text):
    """Imprime el texto en color verde"""
    return "\033[92m{}\033[0m".format(text)

def amarillo(text):
    """Imprime el texto en color amarillo"""
    return "\033[93m{}\033[0m".format(text)

def azul(text):
    """Imprime el texto en color azul"""
    return "\033[94m{}\033[0m".format(text)

def negro(text):
    """Imprime el texto en color negro"""
    return "\033[0;30m{}\033[0m".format(text)

def magenta(text):
    """Imprime el texto en color magenta"""
    return "\033[0;35m{}\033[0m".format(text)

