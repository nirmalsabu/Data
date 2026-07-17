from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_summary_service
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/generate-summary", tags=["summaries"])


@router.post("")
async def generate_summary_endpoint(content: str, db: AsyncSession = Depends(get_db), summary_service: SummaryService = Depends(get_summary_service)):
    return {"summary": await summary_service.generate_summary(content)}
