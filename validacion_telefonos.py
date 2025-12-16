import requests
import pandas as pd

def verificar_numlookup(api_key, numero, codigo_pais=None):
    """
    Usa NumlookupAPI para verificar un número telefónico.
    Retorna diccionario con info, incluyendo tipo de línea.
    """
    url = f"https://api.numlookupapi.com/v1/validate/{numero}"
    headers = {
        "apikey": api_key
    }
    params = {}
    if codigo_pais:
        params["country_code"] = codigo_pais

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return {"numero": numero, "error": f"HTTP {resp.status_code}"}

    data = resp.json()
    tipo = data.get("line_type", "desconocido")
    valid = data.get("valid", False)

    return {
        "numero": numero,
        "valid": valid,
        "tipo_linea": tipo,
        "carrier": data.get("carrier"),
        "pais": data.get("country_name")
    }

def procesar_lista_numlookup(api_key, lista_numeros, codigo_pais=None):
    resultados = []
    for numero in lista_numeros:
        res = verificar_numlookup(api_key, numero, codigo_pais)
        resultados.append(res)
    return resultados

if __name__ == "__main__":
    api_key_numlookup = "TU_API_KEY"

    # Leer los números desde un archivo Excel
    # Si tu archivo tiene encabezado (columna llamada "Numero")
    df_numeros = pd.read_excel("numeros.xlsx")
    numeros = df_numeros.iloc[:, 0].astype(str).tolist()  # toma la primera columna y la convierte en lista de strings

    print("Usando NumlookupAPI con números desde Excel:")
    resultados_nl = procesar_lista_numlookup(api_key_numlookup, numeros, codigo_pais="MX")

    # Mostrar cantidad consultada
    print("Cantidad de teléfonos consultados:")
    print(len(resultados_nl))

    # Mostrar resultados en consola
    for r in resultados_nl:
        print(f"Número: {r['numero']} → Válido: {r['valid']} → Tipo: {r.get('tipo_linea')}")

    # Guardar resultados en un archivo de Excel
    df_resultados = pd.DataFrame(resultados_nl)
    df_resultados.to_excel("resultados_numlookup.xlsx", index=False)
    print("✅ Datos guardados en resultados_numlookup.xlsx")
