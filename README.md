# Validación Masiva de Teléfonos vía API (Numlookup)

Este script en Python automatiza el proceso de limpieza y validación de bases de datos telefónicas mediante la integración con la API REST de **NumlookupAPI**. 

##  Problema vs Solución

* **Problema:** La validación de bases de datos se realizaba de forma manual número por número, consumiendo horas de trabajo operativo y aumentando el riesgo de contactar números inexistentes o de carriers incorrectos.
* **Solución:** Automatización completa del flujo de validación. El script procesa miles de números en minutos, identificando la validez, el carrier y el tipo de línea (móvil/fijo) de forma masiva.

---

##  Tecnologías Utilizadas
* **Python 3**
* **Requests:** Para el consumo de la API REST mediante métodos HTTP GET.
* **Pandas:** Para la lectura de la base original en Excel y la estructuración de los resultados.
* **JSON:** Para el parseo de las respuestas enviadas por el servidor.

---

##  Explicación Paso a Paso del Código

El script funciona como un conector inteligente entre una base de datos local y un servicio de validación global:

### 1. Ingesta y Preparación de Datos
El script utiliza `pandas` para leer el archivo `numeros.xlsx`. Convierte automáticamente la primera columna en una lista de strings para asegurar que los números que comienzan con "0" o códigos de país no pierdan su formato original durante la lectura.

### 2. Consumo de la API (Función `verificar_numlookup`)
Para cada número de la lista, el script realiza una petición segura:
* **Encabezados (Headers):** Autentica la petición usando una `apikey`.
* **Parámetros:** Permite filtrar por código de país (ej. "MX") para aumentar la precisión de la búsqueda.
* **Manejo de Errores:** Incluye una validación del `status_code`. Si la API falla o la key es inválida, el script captura el error en lugar de detenerse.

### 3. Extracción de Atributos Clave
Una vez recibida la respuesta en formato JSON, el código extrae y traduce los puntos de datos más relevantes para el negocio:
* **Valid:** Confirma si el número existe.
* **Line Type:** Determina si es celular o fijo (crucial para campañas de SMS).
* **Carrier:** Identifica la compañía telefónica (Telcel, AT&T, Movistar, etc.).
* **Location:** Confirma el país de origen.

### 4. Procesamiento Iterativo
La función `procesar_lista_numlookup` recorre toda la lista cargada desde el Excel, almacenando cada respuesta en una lista de diccionarios. Esto permite manejar grandes volúmenes de datos de forma organizada antes de la exportación.

### 5. Exportación de Resultados
Finalmente, transforma la lista de resultados nuevamente en un DataFrame de Pandas y genera un archivo `resultados_numlookup.xlsx`. Este archivo final mantiene la integridad de los datos y está listo para ser usado en CRM o campañas de marketing.

---

##  Requisitos y Uso

1.  Obtener una API Key en [NumlookupAPI](https://numlookupapi.com/).
2.  Instalar librerías necesarias:
    ```bash
    pip install requests pandas openpyxl
    ```
3.  Colocar los números en la primera columna de un archivo llamado `numeros.xlsx`.
4.  Reemplazar `"TU_API_KEY"` en el código y ejecutar:
    ```bash
    python validacion_telefonos.py
    ```
