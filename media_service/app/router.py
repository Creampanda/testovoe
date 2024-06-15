from fastapi import APIRouter

router = APIRouter()


@router.get("/memes")
async def get_memes():
    return {"message": "List of memes"}
