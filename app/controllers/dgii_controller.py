from fastapi import APIRouter
import os

from app.services.dgii_service import RNC

router = APIRouter()


@router.get("/")
def get_general():
    return {
        "general": []
    }


@router.get("/rnc")
def get_all_rnc():
    data_route = os.path.join(
        os.path.dirname(__file__), '../../data/dgii/rnc/TMP/DGII_RNC.TXT')

    if not os.path.exists(data_route):
        print("No se encontró el archivo.")
        RNC.get_rnc_list()
    RNC.extract_data()
