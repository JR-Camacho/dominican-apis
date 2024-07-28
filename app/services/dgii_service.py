# Import necessary libraries
import requests
from selenium import webdriver
import zipfile
import os
import pandas as pd

from app.utils.functions import find_links_to_zip_rar_files, parse_url, download_zip_rar_files_from_url

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

# General information services

general_url = "https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx"


class GeneralService:
    def __init__(self, driver=None):
        self.driver = driver


class RNC:
    # Get the rnc list from the DGII website
    def get_rnc_list(url=general_url):
        url = "https://www.dgii.gov.do/app/WebApps/Consultas/RNC/DGII_RNC.zip"

        # Download the ZIP file
        folder_name = f"downloads/dgii/rnc/all"
        download_zip_rar_files_from_url([url], folder_name)

    def extract_data(origin_location='../../downloads/dgii/rnc/all/DGII_RNC.zip', extract_location='../../data/dgii/rnc'):
        print("Extrayendo archivos de", origin_location)

        adjusted_origin_location = os.path.join(
            os.path.dirname(__file__), origin_location)
        ajusted_extract_location = os.path.join(
            os.path.dirname(__file__), extract_location)

        # if os.path.exists(adjusted_origin_location):
        # # if os.path.exists("../downloads/dgii/rnc/all/DGII_RNC.zip"):
        #     print("El archivo ZIP existe.")
        # else:
        #     print("El archivo ZIP no existe.")
        #     return

        # Asegurarse de que el directorio de extracción existe
        os.makedirs(ajusted_extract_location, exist_ok=True)

        # Abrir el archivo ZIP en modo lectura
        with zipfile.ZipFile(adjusted_origin_location, 'r') as zip_ref:
            # Extraer todo el contenido en el directorio especificado
            zip_ref.extractall(ajusted_extract_location)

        # Ahora puedes trabajar con los archivos extraídos como necesites
        # Por ejemplo, listar los archivos extraídos
        extracted_files = os.listdir(ajusted_extract_location)
        print("Archivos extraídos:", extracted_files)

        # Verificar si el archivo existe
        if os.path.isfile(ajusted_extract_location + '/TMP/DGII_RNC.TXT'):
            # Leer el archivo TXT en un DataFrame usando una codificación adecuada y el delimitador '|'
            try:
                df = pd.read_csv(ajusted_extract_location + '/TMP/DGII_RNC.TXT',
                                 delimiter='|', encoding='latin1')  # Usar el delimitador '|'
                print("DataFrame cargado con éxito.")
            except UnicodeDecodeError as e:
                print(f"Error de decodificación: {e}")
        else:
            print(
                f"El archivo {ajusted_extract_location + '/TMP/DGII_RNC.TXT'} no existe.")

        # Asignar los nuevos nombres a las columnas del DataFrame
        df.columns = ['Cédula/RNC', 'Nombre/Razón Social', 'Nombre Comercial', 'Categoría', 'Borrar1',
                      'Borrar2', 'Borrar3', 'Borrar4', 'Fecha Afiliación', 'Estado', 'Régimen de pagos']

        # Eliminar columnas ignoradas
        df.drop(['Borrar1', 'Borrar2', 'Borrar3',
                'Borrar4'], axis=1, inplace=True)

        # return the dataframe
        print("Dataframe listo para ser usado.")
        return df
