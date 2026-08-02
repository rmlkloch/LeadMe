from fastapi import APIRouter
from app.services.reset import reset_demo_environment

router = APIRouter()

@router.post("/reset-demo")
def reset_demo():
    """Manually trigger a full reset of the demo_client_1 environment."""
    reset_demo_environment()
    return {"status": "success", "message": "Demo sandbox environment reset successfully."}
