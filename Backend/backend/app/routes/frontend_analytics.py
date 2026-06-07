from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.services import dashboard_services as svc

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/analyses")
async def list_analyses(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await svc.list_analysis(db,limit,offset)

@router.get("/analyses/{analyses_id}")
async def get_analyses_by_id(analyses_id:int,db:AsyncSession = Depends(get_db)):
    result = await svc.get_analysis_details(db,analyses_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analyses not found")
    return result


@router.get("/stats")
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    return await svc.get_dashboard_stats(db)


@router.get("/risk-distribution")
async def risk_distribution(db: AsyncSession = Depends(get_db)):
    return await svc.get_risk_distribution(db)


@router.get("/top-risky")
async def top_risky_prs(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    return await svc.get_top_risky_prs(db, limit)


@router.get("/recent-activity")
async def recent_activity(
    limit: int = Query(15, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    return await svc.get_recent_activity(db, limit)
