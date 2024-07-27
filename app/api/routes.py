from fastapi import APIRouter

from app.controllers.general_controller import router as general_router
from app.controllers.dgii_controller import router as dgii_router

router = APIRouter()

#Here we add each enpoint  
router.include_router(general_router, prefix="/general", tags=["general"])
router.include_router(dgii_router, prefix="/dgii", tags=["dgii"])