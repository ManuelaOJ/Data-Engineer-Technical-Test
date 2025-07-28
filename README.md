# **Data Extraction and PDF Downloader (Task 1)**

Este proyecto tiene como objetivo extraer archivos PDF desde una URL, descargarlos, organizarlos por trimestre y año, calcular sus hashes SHA256, y almacenar los metadatos en un archivo Parquet para su posterior análisis.

## **Descripción**

El proyecto está dividido en varias tareas:

- **Task 1**: Extrae y descarga archivos PDF de informes financieros de un sitio web específico, organiza los archivos por trimestre (Q1-Q4) y año (2021-2025), calcula su hash SHA256 y guarda los metadatos en un archivo Parquet.


### **Flujo de Trabajo de Task 1**

1. **Extracción de enlaces PDF**: Se obtienen los enlaces de los informes financieros desde una URL proporcionada, filtrando los enlaces de informes trimestrales (Q1-Q4) de los años 2021 a 2025.
2. **Creación de nombres de archivo**: Los enlaces extraídos son descargados y almacenados localmente con nombres limpios (incluyendo año y trimestre, como `Consolidated_Financial_Statements_Q1_2023.pdf`).
3. **Descarga de archivos PDF**: Los archivos PDF se descargan y guardan en directorios organizados por año y trimestre.
4. **Cálculo del hash SHA256**: Se calcula el hash SHA256 de cada archivo PDF descargado para asegurar la integridad del archivo.
5. **Metadatos**: Se extraen metadatos del archivo PDF (nombre, tamaño, hash SHA256, marca temporal de descarga, etc.).
6. **Almacenamiento de metadatos**: Los metadatos se guardan en un archivo Parquet.

## **Requisitos**

El proyecto depende de las siguientes bibliotecas Python. Si no las tienes instaladas, puedes hacerlo ejecutando:


pip install -r requirements.txt


### **Flujo de Trabajo de Task 2**

1. **Lectura del archivo PDF**: Se abre el archivo PDF descargado en **Task 1** usando la librería `pdfplumber`, y se procesan las páginas del informe financiero Q1 2025.
   
2. **Extracción de tablas estructuradas**: Se extraen todas las tablas estructuradas de cada página del informe utilizando la función `extract_tables()` de `pdfplumber`. Se utiliza la estrategia `lines_strict` para asegurar que se capture la estructura de las tablas con precisión.

3. **Conversión a formato largo (long format)**: Cada tabla extraída se convierte en un formato largo, donde cada fila representa un solo dato (es decir, una "celda" de una tabla tradicional se convierte en una fila en un dataframe). Esto se logra usando la función `pd.melt()` de **pandas**.

4. **Adición de metadatos**: Para cada tabla extraída, se agrega la columna `page_number` que indica el número de página en el PDF donde se encontró la tabla.

5. **Verificación de las tablas**: Se verifica que las tablas no estén vacías y que tengan al menos dos filas para ser procesadas.

6. **Salida de los datos**: Las tablas extraídas y convertidas a formato largo se muestran en consola (en este caso, en un ejemplo de impresión).

---

### **Requisitos**

El proyecto depende de las siguientes bibliotecas Python pdfplumber, pandas. Si no las tienes instaladas, puedes hacerlo ejecutando:


pip install -r requirements.txt
