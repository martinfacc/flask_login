def error(cantidad, mensaje):
    for i in range(cantidad):
        print(mensaje)

def mayuscula(lista, parametro):
    for elemento in lista:
        elemento.parametro=elemento.parametro.upper()

def quitar_acento(lista, parametro):
    def normalize(s):
        replacements = (
        ('Á', 'A'),
        ('É', 'E'),
        ('Í', 'I'),
        ('Ó', 'O'),
        ('Ú', 'U'),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    for elemento in lista:
        elemento.parametro=normalize(elemento.parametro)