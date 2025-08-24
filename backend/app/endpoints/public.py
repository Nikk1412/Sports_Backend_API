from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.db.db import get_department_matches, get_points_data

router = APIRouter()

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from app.db.db import get_department_matches_filtered
from fastapi.encoders import jsonable_encoder

import datetime
router = APIRouter()

@router.get("/matches")
async def get_matches(
    is_final: Optional[bool] = False,
    dept: Optional[str] = None,
    year: Optional[int] = None,
    sport: Optional[str] = None,
    top: Optional[int] = None
):
    try:
        filters = {
            "is_final": is_final if is_final else "all",
            "dept": dept if dept else "all",
            "year": year if year else "all",
            "sport": sport if sport else "all",
            "top": top if top else "all"
        }

        data = jsonable_encoder(get_department_matches_filtered(filters))

        return JSONResponse(
            status_code=200,
            content={"message": "Data fetched successfully", "data": data}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/points/{year}")
async def get_points(year: str = "current"):
    try:
        y = datetime.datetime.now().year if year == "current" else int(year)
        data = get_points_data(y)
        return JSONResponse(status_code=200, content={"message": "Data fetched successfully", "data": data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dept_history/{department}")
async def department_history(department: str):
    try:
        return JSONResponse(
                status_code=200,
                content={
                    "message": "Data fetched successfully", 
                    "data": jsonable_encoder(get_department_matches(department))
                }
            )
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid year or department"
        )
            

