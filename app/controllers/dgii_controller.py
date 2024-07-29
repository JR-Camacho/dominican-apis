from fastapi import APIRouter, Query
import os
import json

from app.services.dgii_service import RNC

router = APIRouter()


@router.get("/")
def get_general():
    return {
        "general": []
    }


@router.get("/rnc")
def get_all_rnc(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1)):
    data_route = os.path.join(
        os.path.dirname(__file__), '../../data/dgii/rnc/TMP/DGII_RNC.TXT')

    if not os.path.exists(data_route):
        print("No se encontró el archivo.")
        RNC.get_rnc_list()
    result = RNC.extract_data()

    # # Convertir el DataFrame a un arreglo de objetos JSON
    # json_result = result.to_json(orient='records')

    # # Imprimir el resultado
    # # return json_result
    # return {"all rnc data": json_result}

    # Calcular el total de páginas
    total_rows = len(result)
    total_pages = (total_rows + page_size - 1) // page_size

    # Calcular el rango de filas para la página solicitada
    start_row = (page - 1) * page_size
    end_row = start_row + page_size

    # Filtrar el DataFrame para la paginación
    paginated_result = result.iloc[start_row:end_row]

    # Convertir el DataFrame paginado a un arreglo de objetos JSON
    json_result = paginated_result.to_json(orient='records')

    # Convertir la cadena de texto JSON a un objeto Python
    data_object = json.loads(json_result)

    # Devolver el resultado junto con información de paginación
    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": data_object
    }
