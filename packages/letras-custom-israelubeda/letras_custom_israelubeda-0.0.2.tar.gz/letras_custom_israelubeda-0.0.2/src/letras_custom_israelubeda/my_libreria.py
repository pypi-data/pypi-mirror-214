def sustituir_letras(palabra):
    sustituciones = {
        'a': 'z',
        'b': 'y',
        'c': 'x',
        'd': 'w',
        'e': 'v',
        'f': 'u',
        'g': 't',
        'h': 's',
        'i': 'r',
        'j': 'q',
        'k': 'p',
        'l': 'o',
        'm': 'n',
        # Agrega aquí más sustituciones de letras según tus necesidades
    }
    palabra_sustituida = ''
    for letra in palabra:
        if letra.lower() in sustituciones:
            letra_sustituida = sustituciones[letra.lower()]
            if letra.isupper():
                letra_sustituida = letra_sustituida.upper()
            palabra_sustituida += letra_sustituida
        else:
            palabra_sustituida += letra
    return palabra_sustituida
