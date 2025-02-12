from datetime import date

# Función para calcular el puntaje de edad
def calcular_puntaje_edad(edad):
    edad = int(edad)
    if 20 <= edad <= 25:
        return 5
    elif 26 <= edad <= 35:
        return 10
    elif 36 <= edad <= 50:
        return 15
    elif 51 <= edad <= 65:
        return 20
    else:
        return 0  # Fuera del rango

# Función para calcular el puntaje de ingresos
def calcular_puntaje_ingresos(ingresos):
    ingresos = int(ingresos)
    if ingresos < 3_000_000:
        return 5
    elif 3_000_000 <= ingresos < 5_000_000:
        return 10
    elif 5_000_000 <= ingresos <= 10_000_000:
        return 15
    else:  # ingresos > 10_000_000
        return 20

# Función para calcular el puntaje de faja
def calcular_puntaje_faja(faja):
    faja_dict = {"M-N": 5, "I-L": 10, "E-H": 15, "A-D": 20}
    faja = faja.upper()  # Convertir la letra a mayúscula para consistencia
    for rango, puntaje in faja_dict.items():
        inicio, fin = rango.split("-")  # Dividir el rango en inicio y fin
        if inicio <= faja <= fin:  # Verificar si la letra está en el rango
            return puntaje
    return 0  # Retornar 0 si no pertenece a ningún rango

# Función para calcular el puntaje de antigüedad laboral
def calcular_puntaje_antiguedad(antiguedad):
    puntajes = {
        "6 meses a un año": 5,
        "1 a 2 años": 10,
        "3 a 5 años": 15,
        "Más de 5 años": 20
    }
    
    return puntajes.get(antiguedad, 0)  # Retorna 0 si el parámetro no coincide con ninguna clave

# Función para calcular el puntaje de activos
def calcular_puntaje_activos(activos):
    activos_dict = {
        "ninguno": 5,
        "vehículo": 10,
        "inmueble": 15,
        "vehículo e inmueble": 20
    }
    return activos_dict.get(activos.lower(), 0)  # Retorna 0 si no coincide


def calcular_dti(deudas, ingresos, cuota):
    ingresos = int(ingresos)
    deudas = int(deudas)
    cuota = int(cuota)
    if ingresos == 0:
        return 0
    return ((deudas+cuota)/ingresos)*100 

# Función para calcular el puntaje de ratio deuda/ingreso (DTI)
def calcular_puntaje_dti(dti):
    if dti > 50:
        return 5
    elif 40 <= dti <= 49:
        return 10
    elif 20 <= dti <= 39:
        return 15
    elif dti < 20:
        return 20
    else:
        return 0

# Función para calcular la calificación final
def calcular_calificacion_final(edad, ingresos, faja, antiguedad, activos, deudas, cuota):
    ponderaciones = {
        "edad": 0.10,
        "ingresos": 0.20,
        "faja": 0.20,
        "antiguedad": 0.10,
        "activos": 0.20,
        "dti": 0.20
    }
    
    # Calcular puntajes ponderados
    puntaje_edad = calcular_puntaje_edad(edad) * ponderaciones["edad"]
    puntaje_ingresos = calcular_puntaje_ingresos(ingresos) * ponderaciones["ingresos"]
    puntaje_faja = calcular_puntaje_faja(faja) * ponderaciones["faja"]
    puntaje_antiguedad = calcular_puntaje_antiguedad(antiguedad) * ponderaciones["antiguedad"]
    puntaje_activos = calcular_puntaje_activos(activos) * ponderaciones["activos"]
    puntaje_dti = calcular_puntaje_dti(calcular_dti(deudas, ingresos, cuota)) * ponderaciones["dti"]
    
    # Sumar los puntajes ponderados
    puntaje_total = sum([
        puntaje_edad,
        puntaje_ingresos,
        puntaje_faja,
        puntaje_antiguedad,
        puntaje_activos,
        puntaje_dti
    ])
    
    # Dictamen final
    if 5 <= puntaje_total < 10:
        recomendacion = "No recomendado"
    elif 10 <= puntaje_total < 16:
        recomendacion = "Aprobado con condiciones"
    elif 16 <= puntaje_total <= 20:
        recomendacion = "Aprobado"
    else:
        recomendacion = "No definido"
    
    return puntaje_total, recomendacion




# Ejemplo de uso
if __name__ == "__main__":
    edad = 38
    ingresos = 15_000_000
    faja = "A"
    antiguedad = "3 a 5 años"  
    activos = "Vehículo e Inmueble"
    deudas = 3360000
    cuota = 416000

    puntaje_final, recomendacion = calcular_calificacion_final(edad, ingresos, faja, antiguedad, activos, deudas, cuota)
    print(f"Puntaje Final: {puntaje_final}")
    print(f"Dictamen Final: {recomendacion}")
    print(f"puntaje edad: {calcular_puntaje_edad(edad)}")
    print(f"puntaje dti: {calcular_puntaje_dti(calcular_dti(deudas, ingresos, cuota))}")
    print(f"puntaje Activos: {calcular_puntaje_activos(activos)}")
    print(f"antiguedad: {calcular_puntaje_antiguedad(antiguedad)}")
    print(f"puntaje faja: {calcular_puntaje_faja(faja)}")
    print(f"puntaje ingresos: {calcular_puntaje_ingresos(ingresos)}")