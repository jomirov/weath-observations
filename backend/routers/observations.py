from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..database.observation import Observation
from ..dependencies import identify_user, is_valid_observation, get_obs_dao
from ..database.observationDAO import ObservationDAO


router = APIRouter()

@router.post('/observations')
async def make_observation(o: Observation, obsDAO: ObservationDAO = Depends(get_obs_dao), x_token: str = Header()):
    current_owner_id = identify_user(x_token)
    if current_owner_id == -1:
        raise HTTPException(status_code=401)
    if not is_valid_observation(o):
        raise HTTPException(status_code=422)
    new_observation_id = obsDAO.insert_observation(current_owner_id, o.city, o.temperature_C, o.note)
    return JSONResponse({"status": "OK", "message": f"Observation by {new_observation_id} ID has been created"}, status_code=201)

@router.get('/observations', status_code=200)
async def show_all_observations(obsDAO: ObservationDAO = Depends(get_obs_dao), x_token: str = Header()):
    current_owner_id = identify_user(x_token)
    if current_owner_id == -1:
        raise HTTPException(status_code=401)
    return JSONResponse(obsDAO.get_observations(owner_id=current_owner_id))

@router.get('/observations/{o_id}', status_code=200)
async def show_observation(o_id: int, obsDAO: ObservationDAO = Depends(get_obs_dao), x_token: str = Header()):
    current_owner_id = identify_user(x_token)
    if current_owner_id == -1:
        raise HTTPException(status_code=401)
    o = obsDAO.get_observation_by_id(id=o_id)
    if  o == None or o["owner_id"] != current_owner_id:
        raise HTTPException(status_code=404)
    return JSONResponse(o)

@router.delete('/observations/{o_id}', status_code=200)
async def remove_observation(o_id: int, obsDAO: ObservationDAO = Depends(get_obs_dao), x_token: str = Header()):
    current_owner_id = identify_user(x_token)
    if current_owner_id == -1:
        raise HTTPException(status_code=401)
    o = obsDAO.get_observation_by_id(id=o_id)
    if o == None or o["owner_id"] != current_owner_id:
        raise HTTPException(status_code=404)
    obsDAO.delete_observation_by_id(id=o_id)
    return JSONResponse({"status": "OK", "message": f"Observation by {o_id} ID has been removed"})