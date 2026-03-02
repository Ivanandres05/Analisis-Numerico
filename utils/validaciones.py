def validar_numerico(valor, nombre_campo):
    try:
        return float(valor)
    except ValueError:
        raise ValueError(f"Valores de entrada inválidos: El campo '{nombre_campo}' debe ser un número válido.")

def validar_entero_positivo(valor, nombre_campo):
    try:
        n = int(valor)
        if n <= 0:
            raise ValueError()
        return n
    except ValueError:
        raise ValueError(f"Valores de entrada inválidos: El campo '{nombre_campo}' debe ser un entero positivo.")
