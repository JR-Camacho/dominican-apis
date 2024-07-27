from fastapi import APIRouter

from app.services.dgii_service import RNC

router = APIRouter()

@router.get("/")
def get_general():
    return {
        "general": [] 
    }

@router.get("/rnc")
def get_all_rnc():
    RNC.get_rnc_list()