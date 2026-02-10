from fastapi import APIRouter
from APP.API.V1.ENDPOINTS import enhancement

api_router = APIRouter()

# INCLUDE THE ENHANCEMENT ROUTER
api_router.include_router(
    enhancement.router, 
    prefix="/images", 
    tags=["IMAGE ENHANCEMENT"]
)